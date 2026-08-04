import json
import logging
import os
from datetime import datetime, timezone
from urllib import request, error

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client("sns")
secretsmanager = boto3.client("secretsmanager")
s3 = boto3.client("s3")

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "").strip()
ENABLE_SNS = os.getenv("ENABLE_SNS", "true").lower() == "true"
ENABLE_SLACK = os.getenv("ENABLE_SLACK", "false").lower() == "true"
SLACK_SECRET_ID = os.getenv("SLACK_SECRET_ID", "").strip()
ARCHIVE_BUCKET_NAME = os.getenv("ARCHIVE_BUCKET_NAME", "").strip()
ARCHIVE_PREFIX = os.getenv("ARCHIVE_PREFIX", "security-events/").strip()

SUPPORTED_EVENTS = {
    ("iam.amazonaws.com", "CreateAccessKey"): "HIGH",
    ("iam.amazonaws.com", "DeleteUser"): "HIGH",
    ("s3.amazonaws.com", "DeleteBucket"): "CRITICAL",
}

_cached_webhook_url = None


def get_actor_arn(detail: dict) -> str:
    identity = detail.get("userIdentity", {})
    return (
        identity.get("arn")
        or identity.get("sessionContext", {})
        .get("sessionIssuer", {})
        .get("arn")
        or "UNKNOWN"
    )


def get_webhook_url() -> str:
    global _cached_webhook_url

    if _cached_webhook_url:
        return _cached_webhook_url

    if not SLACK_SECRET_ID:
        raise ValueError("SLACK_SECRET_ID is not configured")

    response = secretsmanager.get_secret_value(SecretId=SLACK_SECRET_ID)
    value = response.get("SecretString", "").strip()

    try:
        parsed = json.loads(value)
        webhook_url = parsed.get("webhook_url", "").strip()
    except json.JSONDecodeError:
        webhook_url = value

    if not webhook_url.startswith("https://hooks.slack.com/"):
        raise ValueError("Invalid Slack webhook URL format")

    _cached_webhook_url = webhook_url
    return webhook_url


def send_slack(payload: dict) -> int:
    webhook = get_webhook_url()
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        webhook,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(req, timeout=8) as response:
        body = response.read().decode("utf-8", errors="replace")
        logger.info("Slack status=%s body=%s", response.status, body)
        return response.status


def publish_sns(subject: str, message: str) -> None:
    if ENABLE_SNS and SNS_TOPIC_ARN:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject[:100],
            Message=message,
        )


def archive_event(event: dict, event_name: str, event_id: str) -> None:
    if not ARCHIVE_BUCKET_NAME:
        return

    timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    key = f"{ARCHIVE_PREFIX}{timestamp}/{event_name}-{event_id}.json"

    s3.put_object(
        Bucket=ARCHIVE_BUCKET_NAME,
        Key=key,
        Body=json.dumps(event, indent=2, default=str).encode("utf-8"),
        ContentType="application/json",
        ServerSideEncryption="AES256",
    )


def build_record(event: dict) -> dict:
    detail = event.get("detail", {})
    event_source = detail.get("eventSource")
    event_name = detail.get("eventName")
    severity = SUPPORTED_EVENTS[(event_source, event_name)]

    record = {
        "project": "Task10_CloudTrail_Security_Monitoring",
        "event_name": event_name,
        "event_source": event_source,
        "severity": severity,
        "actor_arn": get_actor_arn(detail),
        "identity_type": detail.get("userIdentity", {}).get("type", "UNKNOWN"),
        "account_id": event.get("account", detail.get("recipientAccountId", "UNKNOWN")),
        "region": event.get("region", detail.get("awsRegion", "UNKNOWN")),
        "event_time": detail.get("eventTime", event.get("time", "UNKNOWN")),
        "source_ip": detail.get("sourceIPAddress", "UNKNOWN"),
        "user_agent": detail.get("userAgent", "UNKNOWN"),
        "event_id": detail.get("eventID", event.get("id", "UNKNOWN")),
        "request_id": detail.get("requestID", "UNKNOWN"),
        "request_parameters": detail.get("requestParameters") or {},
        "response_elements": detail.get("responseElements"),
    }

    if event_name == "CreateAccessKey":
        access_key = (detail.get("responseElements") or {}).get("accessKey", {})
        key_id = access_key.get("accessKeyId", "")
        record["target_user"] = access_key.get("userName") or (
            detail.get("requestParameters") or {}
        ).get("userName")
        record["access_key_id_masked"] = (
            f"{key_id[:4]}...{key_id[-4:]}" if len(key_id) > 8 else "REDACTED"
        )

    elif event_name == "DeleteUser":
        record["target_user"] = (
            detail.get("requestParameters") or {}
        ).get("userName", "UNKNOWN")

    elif event_name == "DeleteBucket":
        record["bucket_name"] = (
            detail.get("requestParameters") or {}
        ).get("bucketName", "UNKNOWN")

    return record


def build_slack_payload(record: dict) -> dict:
    details = json.dumps(record.get("request_parameters", {}), default=str)

    return {
        "text": f"AWS Security Event: {record['event_name']}",
        "attachments": [
            {
                "color": "#d00000" if record["severity"] == "CRITICAL" else "#ff8c00",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{record['severity']} AWS Security Event",
                        },
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Event*\n`{record['event_name']}`"},
                            {"type": "mrkdwn", "text": f"*Region*\n`{record['region']}`"},
                            {"type": "mrkdwn", "text": f"*Actor*\n`{record['actor_arn']}`"},
                            {"type": "mrkdwn", "text": f"*Source IP*\n`{record['source_ip']}`"},
                            {"type": "mrkdwn", "text": f"*Account*\n`{record['account_id']}`"},
                            {"type": "mrkdwn", "text": f"*Event Time*\n`{record['event_time']}`"},
                        ],
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Request Parameters*\n```{details[:2500]}```",
                        },
                    },
                ],
            }
        ],
    }


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event, default=str))

    detail = event.get("detail", {})
    event_source = detail.get("eventSource")
    event_name = detail.get("eventName")
    event_key = (event_source, event_name)

    if event_key not in SUPPORTED_EVENTS:
        return {
            "statusCode": 200,
            "result": "SKIPPED",
            "reason": f"Unsupported event {event_source}:{event_name}",
        }

    event_region = detail.get("awsRegion") or event.get("region")

    if event_name == "DeleteBucket" and event_region != "us-east-1":
        logger.info("Skipping DeleteBucket outside us-east-1: %s", event_region)
        return {
            "statusCode": 200,
            "result": "SKIPPED",
            "reason": "DeleteBucket event is outside us-east-1",
        }

    record = build_record(event)
    logger.info("SECURITY_EVENT=%s", json.dumps(record, default=str))

    subject = f"{record['severity']}: {record['event_name']} detected"
    message = json.dumps(record, indent=2, default=str)

    try:
        publish_sns(subject, message)

        if ENABLE_SLACK:
            slack_status = send_slack(build_slack_payload(record))
            if slack_status < 200 or slack_status >= 300:
                raise RuntimeError(f"Slack returned status {slack_status}")

        archive_event(event, record["event_name"], record["event_id"])

    except (ClientError, BotoCoreError, ValueError, error.URLError) as exc:
        logger.exception("Notification or archive failed")
        raise RuntimeError(f"Security event processing failed: {exc}") from exc

    return {
        "statusCode": 200,
        "result": "PROCESSED",
        "event_name": record["event_name"],
        "severity": record["severity"],
        "event_id": record["event_id"],
    }
