# Part 4 — EventBridge Rules and Testing

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Rule 1 — IAM Security Events

Use:

```text
eventbridge/iam-security-events.json
```

Pattern:

```json
{
  "source": ["aws.iam"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["iam.amazonaws.com"],
    "eventName": ["CreateAccessKey", "DeleteUser"]
  }
}
```

## Rule 2 — S3 Bucket Deletion in us-east-1

Use:

```text
eventbridge/s3-deletebucket-us-east-1.json
```

Pattern:

```json
{
  "source": ["aws.s3"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "region": ["us-east-1"],
  "detail": {
    "eventSource": ["s3.amazonaws.com"],
    "eventName": ["DeleteBucket"],
    "awsRegion": ["us-east-1"]
  }
}
```

## Add Lambda Target

For each rule:

```text
Target: task10-cloudtrail-security-monitor
```

Ensure EventBridge has Lambda invoke permission.

## Test 1 — Create IAM Access Key

Use only an approved test user:

```bash
aws iam create-access-key \
  --user-name task10-test-user
```

Record the returned key securely, then deactivate and delete it after testing.

## Test 2 — Delete IAM User

Create an empty test user:

```bash
aws iam create-user \
  --user-name task10-delete-test-user
```

Delete:

```bash
aws iam delete-user \
  --user-name task10-delete-test-user
```

## Test 3 — Delete Empty S3 Bucket in us-east-1

Create:

```bash
aws s3api create-bucket \
  --bucket <UNIQUE_TEST_BUCKET> \
  --region us-east-1
```

Delete:

```bash
aws s3api delete-bucket \
  --bucket <UNIQUE_TEST_BUCKET> \
  --region us-east-1
```

The bucket must be empty.

## Verification

For every test:

- Lambda invocation count increases
- CloudWatch log contains the event
- SNS email arrives
- Optional Slack message arrives
- Event ID and actor details are visible

## Checklist

- [ ] IAM EventBridge rule created
- [ ] S3 EventBridge rule created
- [ ] Lambda target attached
- [ ] CreateAccessKey tested
- [ ] DeleteUser tested
- [ ] DeleteBucket tested in us-east-1
- [ ] Notifications verified
- [ ] Test resources cleaned up
