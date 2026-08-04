import json, os
import boto3

cw = boto3.client("cloudwatch")
sns = boto3.client("sns")
NAMESPACE = os.getenv("METRIC_NAMESPACE", "SecureCloudOps")
TOPIC = os.getenv("SNS_TOPIC_ARN", "")

SEVERITY = {
    "CreateUser":"HIGH", "CreateAccessKey":"HIGH", "DeleteUser":"HIGH",
    "DeleteBucket":"CRITICAL", "StopLogging":"CRITICAL", "DeleteTrail":"CRITICAL"
}

def lambda_handler(event, context):
    detail = event.get("detail", {})
    name = detail.get("eventName", "Unknown")
    record = {
        "event_name": name,
        "severity": SEVERITY.get(name, "MEDIUM"),
        "actor": detail.get("userIdentity", {}).get("arn", "UNKNOWN"),
        "source_ip": detail.get("sourceIPAddress", "UNKNOWN"),
        "event_time": detail.get("eventTime", event.get("time")),
        "event_id": detail.get("eventID", event.get("id")),
        "request_parameters": detail.get("requestParameters", {}),
    }
    cw.put_metric_data(Namespace=NAMESPACE, MetricData=[{
        "MetricName":"SecurityEvents","Value":1,"Unit":"Count",
        "Dimensions":[{"Name":"EventName","Value":name},{"Name":"Severity","Value":record["severity"]}]
    }])
    if TOPIC:
        sns.publish(TopicArn=TOPIC, Subject=f"{record['severity']}: {name}", Message=json.dumps(record, indent=2))
    return record
