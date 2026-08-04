import fnmatch
import json
import logging
import os
from urllib import request, error

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

secretsmanager = boto3.client("secretsmanager")

SLACK_SECRET_ID = os.environ["SLACK_SECRET_ID"]
AUTHORIZED_CREATOR_ARNS = [
    value.strip()
    for value in os.getenv("AUTHORIZED_CREATOR_ARNS", "").split(",")
    if value.strip()
]
ALERT_ON_AUTHORIZED = os.getenv("ALERT_ON_AUTHORIZED", "false").lower() == "true"
SLACK_CHANNEL_NAME = os.getenv("SLACK_CHANNEL_NAME", "#aws-security-alerts")

_cached_webhook_url = None


def get_slack_webhook_url() -> str:
    global _cached_webhook_url

    if _cached_webhook_url:
        return _cached_webhook_url

    response = secretsmanager.get_secret_value(SecretId=SLACK_SECRET_ID)
    secret_string = response.get("SecretString", "").strip()

    if not secret_string:
        raise ValueError("Slack webhook secret is empty")

    try:
        parsed = json.loads(secret_string)
        webhook_url = parsed.get("webhook_url", "").strip()
    except json.JSONDecodeError:
        webhook_url = secret_string

    if not webhook_url.startswith("https://hooks.slack.com/"):
        raise ValueError("Slack webhook URL has an unexpected format")

    _cached_webhook_url = webhook_url
    return webhook_url


def is_authorized_creator(creator_arn: str) -> bool:
    if not creator_arn:
        return False

    for allowed_pattern in AUTHORIZED_CREATOR_ARNS:
        if fnmatch.fnmatch(creator_arn, allowed_pattern):
            return True

    return False


def get_creator_arn(detail: dict) -> str:
    identity = detail.get("userIdentity", {})

    return (
        identity.get("arn")
        or identity.get("sessionContext", {})
        .get("sessionIssuer", {})
        .get("arn")
        or "UNKNOWN"
    )


def build_slack_payload(event: dict, authorized: bool) -> dict:
    detail = event.get("detail", {})
    request_parameters = detail.get("requestParameters") or {}
    response_elements = detail.get("responseElements") or {}
    user_identity = detail.get("userIdentity") or {}

    username = (
        request_parameters.get("userName")
        or response_elements.get("user", {}).get("userName")
        or "UNKNOWN"
    )

    creator_arn = get_creator_arn(detail)
    account_id = event.get("account", detail.get("recipientAccountId", "UNKNOWN"))
    event_time = detail.get("eventTime", event.get("time", "UNKNOWN"))
    event_id = detail.get("eventID", event.get("id", "UNKNOWN"))
    source_ip = detail.get("sourceIPAddress", "UNKNOWN")
    region = event.get("region", detail.get("awsRegion", "UNKNOWN"))
    identity_type = user_identity.get("type", "UNKNOWN")
    user_agent = detail.get("userAgent", "UNKNOWN")

    severity = "INFO" if authorized else "CRITICAL"
    status = "Authorized" if authorized else "Unauthorized"

    text = (
        f"{severity}: {status} IAM user creation detected. "
        f"New user: {username}; Creator: {creator_arn}"
    )

    color = "#2eb886" if authorized else "#d00000"

    return {
        "text": text,
        "channel": SLACK_CHANNEL_NAME,
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{'Authorized' if authorized else 'Unauthorized'} IAM User Created",
                        },
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*New IAM User*\n`{username}`",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Severity*\n`{severity}`",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Created By*\n`{creator_arn}`",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Identity Type*\n`{identity_type}`",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*AWS Account*\n`{account_id}`",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Region*\n`{region}`",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Source IP*\n`{source_ip}`",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Event Time*\n`{event_time}`",
                            },
                        ],
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                f"*CloudTrail Event ID*\n`{event_id}`\n\n"
                                f"*User Agent*\n`{user_agent}`"
                            ),
                        },
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "Generated by Task 9 AWS Security Monitoring",
                            }
                        ],
                    },
                ],
            }
        ],
    }


def send_to_slack(payload: dict) -> int:
    webhook_url = get_slack_webhook_url()
    encoded_payload = json.dumps(payload).encode("utf-8")

    req = request.Request(
        webhook_url,
        data=encoded_payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=8) as response:
            status = response.getcode()
            body = response.read().decode("utf-8", errors="replace")
            logger.info("Slack delivery status=%s body=%s", status, body)
            return status
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        logger.error("Slack HTTP error status=%s body=%s", exc.code, body)
        raise
    except error.URLError as exc:
        logger.error("Slack connection failed: %s", exc)
        raise


def lambda_handler(event, context):
    detail = event.get("detail", {})
    event_name = detail.get("eventName")
    event_source = detail.get("eventSource")

    logger.info("Received event: %s", json.dumps(event, default=str))

    if event_source != "iam.amazonaws.com" or event_name != "CreateUser":
        logger.info(
            "Skipping eventSource=%s eventName=%s",
            event_source,
            event_name,
        )
        return {
            "statusCode": 200,
            "result": "SKIPPED",
            "reason": "Not an IAM CreateUser event",
        }

    creator_arn = get_creator_arn(detail)
    authorized = is_authorized_creator(creator_arn)

    if authorized and not ALERT_ON_AUTHORIZED:
        logger.info("Authorized IAM user creation by %s; no alert sent", creator_arn)
        return {
            "statusCode": 200,
            "result": "AUTHORIZED_NO_ALERT",
            "creator_arn": creator_arn,
        }

    payload = build_slack_payload(event, authorized)

    try:
        slack_status = send_to_slack(payload)
    except (ClientError, BotoCoreError, ValueError, error.URLError) as exc:
        logger.exception("Security alert delivery failed")
        raise RuntimeError(f"Slack security alert failed: {exc}") from exc

    if slack_status < 200 or slack_status >= 300:
        raise RuntimeError(f"Slack returned unexpected status {slack_status}")

    result = {
        "statusCode": 200,
        "result": "ALERT_SENT",
        "authorized": authorized,
        "creator_arn": creator_arn,
        "slack_status": slack_status,
        "event_id": detail.get("eventID", event.get("id")),
    }

    logger.info("Security alert result: %s", json.dumps(result))
    return result
