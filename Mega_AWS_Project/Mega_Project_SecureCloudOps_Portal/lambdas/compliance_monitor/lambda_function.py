import json, os
from datetime import datetime, timezone
import boto3

ec2 = boto3.client("ec2")
iam = boto3.client("iam")
cw = boto3.client("cloudwatch")
sns = boto3.client("sns")
NAMESPACE = os.getenv("METRIC_NAMESPACE", "SecureCloudOps")
TOPIC = os.getenv("SNS_TOPIC_ARN", "")
REQUIRED_TAGS = os.getenv("REQUIRED_TAGS", "Environment,Owner,Project").split(",")
MAX_KEY_AGE = int(os.getenv("MAX_ACCESS_KEY_AGE_DAYS", "90"))

def lambda_handler(event, context):
    findings = []
    for page in ec2.get_paginator("describe_instances").paginate():
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                tags = {x["Key"]: x.get("Value","") for x in instance.get("Tags",[])}
                missing = [t for t in REQUIRED_TAGS if not tags.get(t)]
                if missing:
                    findings.append({"type":"EC2_TAGS","id":instance["InstanceId"],"missing":missing})
    for page in ec2.get_paginator("describe_volumes").paginate():
        for volume in page["Volumes"]:
            if not volume.get("Encrypted"):
                findings.append({"type":"EBS_ENCRYPTION","id":volume["VolumeId"]})
    now = datetime.now(timezone.utc)
    for upage in iam.get_paginator("list_users").paginate():
        for user in upage["Users"]:
            for kpage in iam.get_paginator("list_access_keys").paginate(UserName=user["UserName"]):
                for key in kpage["AccessKeyMetadata"]:
                    if key["Status"] == "Active":
                        age = (now-key["CreateDate"]).days
                        if age > MAX_KEY_AGE:
                            findings.append({"type":"OLD_ACCESS_KEY","user":user["UserName"],"age_days":age})
    score = max(0, 100 - min(100, len(findings)*10))
    cw.put_metric_data(Namespace=NAMESPACE, MetricData=[
        {"MetricName":"ComplianceScore","Value":score,"Unit":"Percent"},
        {"MetricName":"NonCompliantResources","Value":len(findings),"Unit":"Count"},
    ])
    if findings and TOPIC:
        sns.publish(TopicArn=TOPIC, Subject=f"SecureCloudOps: {len(findings)} compliance findings", Message=json.dumps(findings, indent=2))
    return {"score":score,"findings":findings}
