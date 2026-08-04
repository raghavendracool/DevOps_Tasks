import json
import logging
import os
from urllib.parse import unquote_plus

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

SOURCE_PREFIX = os.environ.get("SOURCE_PREFIX", "incoming/")
FINANCE_PREFIX = os.environ.get("FINANCE_PREFIX", "Finance/")
NON_FINANCE_PREFIX = os.environ.get("NON_FINANCE_PREFIX", "Non-Finance/")


def classify_filename(filename: str) -> str:
    """Return the destination prefix based on the filename."""
    return FINANCE_PREFIX if filename.lower().startswith("fin_") else NON_FINANCE_PREFIX


def object_exists(bucket: str, key: str) -> bool:
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")
        if error_code in {"404", "NoSuchKey", "NotFound"}:
            return False
        raise


def move_object(bucket: str, source_key: str, destination_key: str) -> None:
    copy_source = {"Bucket": bucket, "Key": source_key}

    s3.copy_object(
        Bucket=bucket,
        CopySource=copy_source,
        Key=destination_key,
        MetadataDirective="COPY",
    )

    s3.delete_object(Bucket=bucket, Key=source_key)


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    processed = []
    skipped = []
    failed = []

    for record in event.get("Records", []):
        try:
            bucket = record["s3"]["bucket"]["name"]
            source_key = unquote_plus(record["s3"]["object"]["key"])

            if not source_key.startswith(SOURCE_PREFIX):
                logger.info("Skipping object outside source prefix: %s", source_key)
                skipped.append(source_key)
                continue

            filename = source_key.rsplit("/", 1)[-1]

            if not filename:
                logger.info("Skipping folder marker: %s", source_key)
                skipped.append(source_key)
                continue

            if not object_exists(bucket, source_key):
                logger.info("Source object no longer exists; skipping duplicate event: %s", source_key)
                skipped.append(source_key)
                continue

            destination_prefix = classify_filename(filename)
            destination_key = f"{destination_prefix}{filename}"

            if destination_key == source_key:
                logger.info("Source and destination are identical; skipping: %s", source_key)
                skipped.append(source_key)
                continue

            move_object(bucket, source_key, destination_key)

            message = {
                "source": source_key,
                "destination": destination_key,
                "bucket": bucket,
            }
            processed.append(message)
            logger.info(
                "Classified %s as %s",
                source_key,
                destination_key,
            )

        except Exception as exc:
            logger.exception("Failed to process record")
            failed.append({
                "record": record,
                "error": str(exc),
            })

    response = {
        "processed": processed,
        "skipped": skipped,
        "failed": failed,
    }

    if failed:
        raise RuntimeError(json.dumps(response))

    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }
