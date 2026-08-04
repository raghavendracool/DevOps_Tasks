import json, logging, os
from urllib.parse import unquote_plus
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.client("s3")
cw = boto3.client("cloudwatch")
NAMESPACE = os.getenv("METRIC_NAMESPACE", "SecureCloudOps")

def lambda_handler(event, context):
    processed = 0
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        if not key.startswith("uploads/"):
            continue
        parts = key.split("/", 2)
        if len(parts) < 3:
            continue
        user_id, filename = parts[1], parts[2]
        category = "finance" if filename.lower().startswith("fin_") else "non-finance"
        destination = f"classified/{category}/{user_id}/{filename}"
        s3.copy_object(Bucket=bucket, CopySource={"Bucket": bucket, "Key": key}, Key=destination, MetadataDirective="COPY")
        s3.delete_object(Bucket=bucket, Key=key)
        processed += 1
        logger.info(json.dumps({"source": key, "destination": destination, "category": category}))
    cw.put_metric_data(Namespace=NAMESPACE, MetricData=[{"MetricName":"FileClassificationSuccess","Value":processed,"Unit":"Count"}])
    return {"processed": processed}
