import json
import logging
import os
from datetime import datetime, timezone
from ipaddress import ip_network
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cloudwatch = boto3.client("cloudwatch")
iam = boto3.client("iam")
s3control = boto3.client("s3control")
sns = boto3.client("sns")
s3 = boto3.client("s3")
sts = boto3.client("sts")

METRIC_NAMESPACE = os.getenv("METRIC_NAMESPACE", "SecOps/Compliance")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "").strip()
REPORT_BUCKET = os.getenv("REPORT_BUCKET", "").strip()
REPORT_PREFIX = os.getenv("REPORT_PREFIX", "compliance-reports/").strip()
SCAN_REGIONS = [
    value.strip()
    for value in os.getenv("SCAN_REGIONS", os.getenv("AWS_REGION", "ap-south-1")).split(",")
    if value.strip()
]
MAX_ACCESS_KEY_AGE_DAYS = int(os.getenv("MAX_ACCESS_KEY_AGE_DAYS", "90"))
MIN_PASSWORD_LENGTH = int(os.getenv("MIN_PASSWORD_LENGTH", "14"))
REQUIRE_PASSWORD_REUSE_PREVENTION = (
    os.getenv("REQUIRE_PASSWORD_REUSE_PREVENTION", "true").lower() == "true"
)
ADMIN_PORTS = {
    int(value.strip())
    for value in os.getenv("ADMIN_PORTS", "22,3389").split(",")
    if value.strip()
}
ALERT_ON_NON_COMPLIANT = (
    os.getenv("ALERT_ON_NON_COMPLIANT", "true").lower() == "true"
)


def metric(name: str, value: float, dimensions: list[dict] | None = None, unit: str = "Count"):
    return {
        "MetricName": name,
        "Value": value,
        "Unit": unit,
        "Dimensions": dimensions or [],
    }


def publish_metrics(metric_data: list[dict]) -> None:
    for index in range(0, len(metric_data), 1000):
        cloudwatch.put_metric_data(
            Namespace=METRIC_NAMESPACE,
            MetricData=metric_data[index:index + 1000],
        )


def control_result(control_id: str, title: str, compliant: bool, severity: str, details: dict):
    return {
        "control_id": control_id,
        "title": title,
        "compliant": compliant,
        "severity": severity,
        "details": details,
    }


def generate_credential_report() -> list[dict]:
    try:
        iam.generate_credential_report()
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") not in {
            "ReportInProgress",
            "LimitExceeded",
        }:
            raise

    response = iam.get_credential_report()
    content = response["Content"].decode("utf-8")

    import csv
    import io

    return list(csv.DictReader(io.StringIO(content)))


def check_root_mfa() -> dict:
    rows = generate_credential_report()
    root = next(row for row in rows if row["user"] == "<root_account>")
    enabled = root.get("mfa_active") == "true"
    return control_result(
        "IAM_ROOT_MFA",
        "Root account MFA is enabled",
        enabled,
        "CRITICAL",
        {"mfa_active": enabled},
    )


def check_password_policy() -> dict:
    try:
        policy = iam.get_account_password_policy()["PasswordPolicy"]
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "NoSuchEntity":
            policy = {}
        else:
            raise

    reuse_ok = (
        policy.get("PasswordReusePrevention", 0) >= 24
        if REQUIRE_PASSWORD_REUSE_PREVENTION
        else True
    )

    checks = {
        "minimum_length": policy.get("MinimumPasswordLength", 0) >= MIN_PASSWORD_LENGTH,
        "require_uppercase": policy.get("RequireUppercaseCharacters", False),
        "require_lowercase": policy.get("RequireLowercaseCharacters", False),
        "require_numbers": policy.get("RequireNumbers", False),
        "require_symbols": policy.get("RequireSymbols", False),
        "reuse_prevention": reuse_ok,
    }

    return control_result(
        "IAM_PASSWORD_POLICY",
        "IAM password policy meets configured baseline",
        all(checks.values()),
        "HIGH",
        {"policy": policy, "checks": checks},
    )


def check_old_access_keys() -> dict:
    now = datetime.now(timezone.utc)
    old_keys = []

    user_paginator = iam.get_paginator("list_users")
    for user_page in user_paginator.paginate():
        for user in user_page.get("Users", []):
            key_paginator = iam.get_paginator("list_access_keys")
            for key_page in key_paginator.paginate(UserName=user["UserName"]):
                for key in key_page.get("AccessKeyMetadata", []):
                    if key.get("Status") != "Active":
                        continue
                    age_days = (now - key["CreateDate"]).total_seconds() / 86400
                    if age_days > MAX_ACCESS_KEY_AGE_DAYS:
                        old_keys.append({
                            "user": user["UserName"],
                            "access_key_id": f"{key['AccessKeyId'][:4]}...{key['AccessKeyId'][-4:]}",
                            "age_days": round(age_days, 2),
                        })

    return control_result(
        "IAM_OLD_ACCESS_KEYS",
        "Active access keys meet rotation age",
        len(old_keys) == 0,
        "HIGH",
        {"maximum_days": MAX_ACCESS_KEY_AGE_DAYS, "old_keys": old_keys},
    )


def check_account_public_access_block(account_id: str) -> dict:
    try:
        config = s3control.get_public_access_block(AccountId=account_id)["PublicAccessBlockConfiguration"]
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "NoSuchPublicAccessBlockConfiguration":
            config = {}
        else:
            raise

    required = [
        "BlockPublicAcls",
        "IgnorePublicAcls",
        "BlockPublicPolicy",
        "RestrictPublicBuckets",
    ]
    compliant = all(config.get(key, False) for key in required)

    return control_result(
        "S3_PUBLIC_ACCESS_BLOCK",
        "Account-level S3 Public Access Block is enabled",
        compliant,
        "CRITICAL",
        {"configuration": config},
    )


def check_region(region: str) -> list[dict]:
    ec2 = boto3.client("ec2", region_name=region)
    config_client = boto3.client("config", region_name=region)
    cloudtrail = boto3.client("cloudtrail", region_name=region)

    controls = []

    trails = cloudtrail.describe_trails(includeShadowTrails=False).get("trailList", [])
    multiregion = [trail for trail in trails if trail.get("IsMultiRegionTrail")]
    controls.append(control_result(
        "CLOUDTRAIL_MULTI_REGION",
        f"Multi-region CloudTrail exists in {region}",
        bool(multiregion),
        "CRITICAL",
        {"region": region, "trails": [t.get("Name") for t in multiregion]},
    ))

    validation_disabled = [
        trail.get("Name")
        for trail in trails
        if not trail.get("LogFileValidationEnabled", False)
    ]
    controls.append(control_result(
        "CLOUDTRAIL_LOG_VALIDATION",
        f"CloudTrail log validation is enabled in {region}",
        len(validation_disabled) == 0 and bool(trails),
        "HIGH",
        {"region": region, "validation_disabled_trails": validation_disabled},
    ))

    recorders = config_client.describe_configuration_recorders().get("ConfigurationRecorders", [])
    status = config_client.describe_configuration_recorder_status().get("ConfigurationRecordersStatus", [])
    recording_names = {
        item["name"]
        for item in status
        if item.get("recording")
    }
    controls.append(control_result(
        "CONFIG_RECORDER",
        f"AWS Config recorder is active in {region}",
        bool(recorders) and any(r["name"] in recording_names for r in recorders),
        "HIGH",
        {
            "region": region,
            "recorders": [r["name"] for r in recorders],
            "recording": sorted(recording_names),
        },
    ))

    risky_rules = []
    paginator = ec2.get_paginator("describe_security_groups")
    for page in paginator.paginate():
        for group in page.get("SecurityGroups", []):
            for permission in group.get("IpPermissions", []):
                from_port = permission.get("FromPort")
                to_port = permission.get("ToPort")
                if from_port is None or to_port is None:
                    continue
                admin_exposed = any(from_port <= port <= to_port for port in ADMIN_PORTS)
                if not admin_exposed:
                    continue
                for ip_range in permission.get("IpRanges", []):
                    if ip_range.get("CidrIp") == "0.0.0.0/0":
                        risky_rules.append({
                            "group_id": group["GroupId"],
                            "cidr": "0.0.0.0/0",
                            "from_port": from_port,
                            "to_port": to_port,
                        })
                for ip_range in permission.get("Ipv6Ranges", []):
                    if ip_range.get("CidrIpv6") == "::/0":
                        risky_rules.append({
                            "group_id": group["GroupId"],
                            "cidr": "::/0",
                            "from_port": from_port,
                            "to_port": to_port,
                        })

    controls.append(control_result(
        "SECURITY_GROUP_ADMIN_PORTS",
        f"Administrative ports are not open to the world in {region}",
        len(risky_rules) == 0,
        "CRITICAL",
        {"region": region, "risky_rules": risky_rules},
    ))

    return controls


def process_security_event(event: dict) -> dict:
    detail = event.get("detail", {})
    event_name = detail.get("eventName", "Unknown")
    severity = "CRITICAL" if event_name in {
        "ConsoleLogin",
        "StopLogging",
        "DeleteTrail",
        "DisableKey",
        "ScheduleKeyDeletion",
    } else "HIGH"

    publish_metrics([
        metric(
            "UnauthorizedActivities",
            1,
            [
                {"Name": "EventName", "Value": event_name},
                {"Name": "Severity", "Value": severity},
            ],
        )
    ])

    record = {
        "type": "SECURITY_EVENT",
        "event_name": event_name,
        "severity": severity,
        "account": event.get("account"),
        "region": event.get("region"),
        "event_time": detail.get("eventTime", event.get("time")),
        "actor": detail.get("userIdentity", {}).get("arn", "UNKNOWN"),
        "source_ip": detail.get("sourceIPAddress", "UNKNOWN"),
        "event_id": detail.get("eventID", event.get("id")),
    }

    logger.warning("SECURITY_EVENT=%s", json.dumps(record))

    if SNS_TOPIC_ARN:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"{severity}: AWS security event {event_name}"[:100],
            Message=json.dumps(record, indent=2),
        )

    return record


def lambda_handler(event, context):
    if event.get("detail-type") == "AWS API Call via CloudTrail":
        return {
            "statusCode": 200,
            "result": process_security_event(event),
        }

    account_id = sts.get_caller_identity()["Account"]
    controls = []

    controls.append(check_root_mfa())
    controls.append(check_password_policy())
    controls.append(check_old_access_keys())
    controls.append(check_account_public_access_block(account_id))

    for region in SCAN_REGIONS:
        controls.extend(check_region(region))

    total = len(controls)
    failed = [control for control in controls if not control["compliant"]]
    passed = total - len(failed)
    critical = sum(
        control["severity"] == "CRITICAL"
        for control in failed
    )
    score = round((passed / total) * 100, 2) if total else 0.0

    metric_data = [
        metric("ComplianceScore", score, unit="Percent"),
        metric("TotalControlsEvaluated", total),
        metric("NonCompliantControls", len(failed)),
        metric("CriticalFindings", critical),
        metric("PartialScan", 0),
    ]

    region_counts = {}
    for control in failed:
        details = control.get("details", {})
        region = details.get("region", "GLOBAL")
        region_counts[region] = region_counts.get(region, 0) + 1

        metric_data.append(metric(
            "ControlNonCompliant",
            1,
            [
                {"Name": "ControlId", "Value": control["control_id"]},
                {"Name": "Severity", "Value": control["severity"]},
            ],
        ))

    for region, count in region_counts.items():
        metric_data.append(metric(
            "RegionNonCompliantResources",
            count,
            [{"Name": "Region", "Value": region}],
        ))

    publish_metrics(metric_data)

    report = {
        "project": "Task12_AWS_SecOps_Monitoring",
        "account_id": account_id,
        "request_id": context.aws_request_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scan_regions": SCAN_REGIONS,
        "summary": {
            "compliance_score": score,
            "total_controls": total,
            "passed_controls": passed,
            "non_compliant_controls": len(failed),
            "critical_findings": critical,
        },
        "controls": controls,
    }

    logger.info("COMPLIANCE_REPORT=%s", json.dumps(report, default=str))

    if REPORT_BUCKET:
        key = (
            f"{REPORT_PREFIX}"
            f"{datetime.now(timezone.utc).strftime('%Y/%m/%d')}/"
            f"{context.aws_request_id}.json"
        )
        s3.put_object(
            Bucket=REPORT_BUCKET,
            Key=key,
            Body=json.dumps(report, indent=2, default=str).encode("utf-8"),
            ContentType="application/json",
            ServerSideEncryption="AES256",
        )

    if failed and ALERT_ON_NON_COMPLIANT and SNS_TOPIC_ARN:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"AWS SecOps: {len(failed)} compliance violation(s)"[:100],
            Message=json.dumps(report, indent=2, default=str),
        )

    return {
        "statusCode": 200,
        "compliance_score": score,
        "non_compliant_controls": len(failed),
        "critical_findings": critical,
        "body": json.dumps(report, default=str),
    }
