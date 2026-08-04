import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

iam = boto3.client("iam")
sns = boto3.client("sns")

REQUIRED_TAGS = [
    value.strip()
    for value in os.getenv(
        "REQUIRED_TAGS",
        "Environment,Owner,Project,CostCenter",
    ).split(",")
    if value.strip()
]

MAX_ACCESS_KEY_AGE_DAYS = int(os.getenv("MAX_ACCESS_KEY_AGE_DAYS", "2"))
SCAN_REGIONS = [
    value.strip()
    for value in os.getenv(
        "SCAN_REGIONS",
        os.getenv("AWS_REGION", "ap-south-1"),
    ).split(",")
    if value.strip()
]
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "").strip()
NOTIFY_ON_COMPLIANT = os.getenv("NOTIFY_ON_COMPLIANT", "false").lower() == "true"
MIN_REMAINING_TIME_MS = int(os.getenv("MIN_REMAINING_TIME_MS", "3000"))


def remaining_time_is_low(context: Any) -> bool:
    return context.get_remaining_time_in_millis() < MIN_REMAINING_TIME_MS


def tags_to_dict(tags: list[dict[str, str]] | None) -> dict[str, str]:
    return {
        tag.get("Key", ""): tag.get("Value", "")
        for tag in (tags or [])
        if tag.get("Key")
    }


def mask_access_key(access_key_id: str) -> str:
    if len(access_key_id) <= 8:
        return "REDACTED"
    return f"{access_key_id[:4]}...{access_key_id[-4:]}"


def check_ec2_tags(region: str, context: Any) -> tuple[list[dict], list[str], bool]:
    ec2 = boto3.client("ec2", region_name=region)
    findings: list[dict] = []
    errors: list[str] = []
    partial = False

    paginator = ec2.get_paginator("describe_instances")

    try:
        for page in paginator.paginate():
            if remaining_time_is_low(context):
                partial = True
                break

            for reservation in page.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    tag_map = tags_to_dict(instance.get("Tags"))
                    missing_tags = [
                        tag_key
                        for tag_key in REQUIRED_TAGS
                        if not tag_map.get(tag_key, "").strip()
                    ]

                    if missing_tags:
                        findings.append({
                            "resource_type": "EC2_INSTANCE",
                            "resource_id": instance["InstanceId"],
                            "region": region,
                            "state": instance.get("State", {}).get("Name"),
                            "rule": "REQUIRED_TAGS",
                            "required_tags": REQUIRED_TAGS,
                            "missing_or_empty_tags": missing_tags,
                        })
    except (ClientError, BotoCoreError) as exc:
        errors.append(f"EC2 tag scan failed in {region}: {exc}")

    return findings, errors, partial


def check_ebs_encryption(region: str, context: Any) -> tuple[list[dict], list[str], bool]:
    ec2 = boto3.client("ec2", region_name=region)
    findings: list[dict] = []
    errors: list[str] = []
    partial = False

    paginator = ec2.get_paginator("describe_volumes")

    try:
        for page in paginator.paginate():
            if remaining_time_is_low(context):
                partial = True
                break

            for volume in page.get("Volumes", []):
                if not volume.get("Encrypted", False):
                    findings.append({
                        "resource_type": "EBS_VOLUME",
                        "resource_id": volume["VolumeId"],
                        "region": region,
                        "state": volume.get("State"),
                        "size_gib": volume.get("Size"),
                        "volume_type": volume.get("VolumeType"),
                        "rule": "EBS_ENCRYPTION",
                    })
    except (ClientError, BotoCoreError) as exc:
        errors.append(f"EBS encryption scan failed in {region}: {exc}")

    return findings, errors, partial


def check_iam_access_keys(context: Any) -> tuple[list[dict], list[str], bool]:
    findings: list[dict] = []
    errors: list[str] = []
    partial = False
    now = datetime.now(timezone.utc)

    try:
        user_paginator = iam.get_paginator("list_users")

        for user_page in user_paginator.paginate():
            for user in user_page.get("Users", []):
                if remaining_time_is_low(context):
                    partial = True
                    return findings, errors, partial

                username = user["UserName"]
                key_paginator = iam.get_paginator("list_access_keys")

                for key_page in key_paginator.paginate(UserName=username):
                    for key in key_page.get("AccessKeyMetadata", []):
                        if key.get("Status") != "Active":
                            continue

                        create_date = key["CreateDate"]
                        age = now - create_date
                        age_days = age.total_seconds() / 86400

                        if age_days > MAX_ACCESS_KEY_AGE_DAYS:
                            findings.append({
                                "resource_type": "IAM_ACCESS_KEY",
                                "resource_id": mask_access_key(key["AccessKeyId"]),
                                "user_name": username,
                                "status": key.get("Status"),
                                "created_at": create_date.isoformat(),
                                "age_days": round(age_days, 2),
                                "maximum_days": MAX_ACCESS_KEY_AGE_DAYS,
                                "rule": "ACCESS_KEY_ROTATION",
                            })
    except (ClientError, BotoCoreError) as exc:
        errors.append(f"IAM access-key scan failed: {exc}")

    return findings, errors, partial


def publish_notification(report: dict) -> None:
    if not SNS_TOPIC_ARN:
        return

    total = report["summary"]["total_non_compliant"]
    subject = (
        f"AWS Compliance Alert: {total} violation(s)"
        if total
        else "AWS Compliance Report: Compliant"
    )

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject[:100],
        Message=json.dumps(report, indent=2, default=str),
    )


def lambda_handler(event, context):
    started_at = datetime.now(timezone.utc)
    findings: list[dict] = []
    errors: list[str] = []
    partial_scan = False
    scanned_regions: list[str] = []

    for region in SCAN_REGIONS:
        if remaining_time_is_low(context):
            partial_scan = True
            break

        scanned_regions.append(region)

        ec2_findings, ec2_errors, ec2_partial = check_ec2_tags(region, context)
        findings.extend(ec2_findings)
        errors.extend(ec2_errors)
        partial_scan = partial_scan or ec2_partial

        if remaining_time_is_low(context):
            partial_scan = True
            break

        ebs_findings, ebs_errors, ebs_partial = check_ebs_encryption(region, context)
        findings.extend(ebs_findings)
        errors.extend(ebs_errors)
        partial_scan = partial_scan or ebs_partial

    if not remaining_time_is_low(context):
        iam_findings, iam_errors, iam_partial = check_iam_access_keys(context)
        findings.extend(iam_findings)
        errors.extend(iam_errors)
        partial_scan = partial_scan or iam_partial
    else:
        partial_scan = True

    ec2_count = sum(item["resource_type"] == "EC2_INSTANCE" for item in findings)
    ebs_count = sum(item["resource_type"] == "EBS_VOLUME" for item in findings)
    iam_count = sum(item["resource_type"] == "IAM_ACCESS_KEY" for item in findings)

    completed_at = datetime.now(timezone.utc)

    report = {
        "project": "Task7_AWS_Compliance_Monitoring",
        "account_id": context.invoked_function_arn.split(":")[4],
        "function_name": context.function_name,
        "request_id": context.aws_request_id,
        "started_at": started_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "duration_seconds": round((completed_at - started_at).total_seconds(), 3),
        "scanned_regions": scanned_regions,
        "configured_regions": SCAN_REGIONS,
        "required_tags": REQUIRED_TAGS,
        "maximum_access_key_age_days": MAX_ACCESS_KEY_AGE_DAYS,
        "partial_scan": partial_scan,
        "compliance_status": "NON_COMPLIANT" if findings else "COMPLIANT",
        "summary": {
            "ec2_missing_required_tags": ec2_count,
            "ebs_unencrypted": ebs_count,
            "iam_access_keys_over_age": iam_count,
            "total_non_compliant": len(findings),
            "errors": len(errors),
        },
        "findings": findings,
        "errors": errors,
    }

    logger.info("COMPLIANCE_REPORT=%s", json.dumps(report, default=str))

    if findings or errors or NOTIFY_ON_COMPLIANT:
        try:
            publish_notification(report)
        except (ClientError, BotoCoreError) as exc:
            logger.exception("SNS notification failed: %s", exc)
            report["errors"].append(f"SNS notification failed: {exc}")

    return {
        "statusCode": 200,
        "compliance_status": report["compliance_status"],
        "total_non_compliant": len(findings),
        "partial_scan": partial_scan,
        "body": json.dumps(report, default=str),
    }
