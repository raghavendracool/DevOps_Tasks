# Part 4 — EventBridge Schedule, Testing and Monitoring

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Step 1 — Test Lambda Manually

Create a test event:

```json
{
  "source": "manual-test",
  "detail": {
    "project": "task7"
  }
}
```

Run the test.

Expected result:

```json
{
  "statusCode": 200,
  "compliance_status": "COMPLIANT or NON_COMPLIANT",
  "total_non_compliant": 0
}
```

## Step 2 — Check CloudWatch Logs

Open:

```text
CloudWatch → Log groups
→ /aws/lambda/task7-compliance-monitor
```

The report includes:

- Scan start and end times
- Regions scanned
- EC2 tag violations
- EBS encryption violations
- IAM access-key violations
- Errors
- Partial-scan status
- Total duration

## Step 3 — Create EventBridge Scheduler

Open:

```text
Amazon EventBridge → Scheduler → Create schedule
```

Configure:

```text
Schedule name: task7-compliance-schedule
Schedule pattern: Recurring
Rate expression: rate(15 minutes)
Flexible time window: Off
Target: AWS Lambda Invoke
Function: task7-compliance-monitor
```

Configure retries:

```text
Maximum event age: 1 hour
Maximum retry attempts: 2
```

EventBridge Scheduler requires permission to invoke the Lambda target.

## Step 4 — Verify Scheduled Invocation

After the scheduled time:

- Check Lambda invocation count
- Check CloudWatch Logs
- Check SNS email
- Review Lambda errors and duration

## Step 5 — Create CloudWatch Alarms

Recommended:

### Lambda Errors

```text
Metric: Errors
Threshold: >= 1
Period: 5 minutes
```

### Lambda Duration

Because timeout is 30 seconds:

```text
Metric: Duration
Threshold: >= 25000 ms
```

### Lambda Throttles

```text
Metric: Throttles
Threshold: >= 1
```

## Step 6 — Test Each Violation

### EC2 Tag Test

Remove one required tag from a test EC2 instance.

Run Lambda and confirm it appears in the report.

### EBS Test

Use an existing unencrypted training volume where permitted.

Do not create insecure production resources solely for testing.

### IAM Access-Key Test

Because waiting two days is inconvenient, temporarily set:

```text
MAX_ACCESS_KEY_AGE_DAYS=0
```

Run the test, validate the output, then restore:

```text
MAX_ACCESS_KEY_AGE_DAYS=2
```

## Checklist

- [ ] Manual Lambda test successful
- [ ] CloudWatch report visible
- [ ] EventBridge schedule created
- [ ] Scheduled invocation observed
- [ ] SNS alert received
- [ ] Lambda Errors alarm created
- [ ] Duration alarm created
- [ ] Test value restored to 2 days
