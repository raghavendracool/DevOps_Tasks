# Part 2 — IAM, SNS, S3 and Lambda Setup

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Create SNS Topic

```text
Topic name: task12-secops-alerts
Type: Standard
```

Create and confirm an email subscription.

## Step 2 — Create Report Bucket

Recommended settings:

```text
Block Public Access: Enabled
Versioning: Enabled
Default encryption: SSE-S3 or SSE-KMS
Lifecycle: Archive or expire old reports according to policy
```

Example name:

```text
task12-secops-reports-<unique>
```

## Step 3 — Create Lambda Role

Create:

```text
Role name: task12-secops-lambda-role
Trusted service: Lambda
```

Attach:

```text
AWSLambdaBasicExecutionRole
```

Add the supplied policy:

```text
iam/lambda-policy.json
```

## Step 4 — Create Lambda

```text
Function name: task12-secops-compliance-engine
Runtime: Python 3.12
Memory: 256 MB
Timeout: 60 seconds
```

## Step 5 — Environment Variables

| Variable | Example |
|---|---|
| `METRIC_NAMESPACE` | `SecOps/Compliance` |
| `SNS_TOPIC_ARN` | SNS topic ARN |
| `REPORT_BUCKET` | Report bucket |
| `REPORT_PREFIX` | `compliance-reports/` |
| `SCAN_REGIONS` | `ap-south-1,us-east-1` |
| `MAX_ACCESS_KEY_AGE_DAYS` | `90` |
| `MIN_PASSWORD_LENGTH` | `14` |
| `REQUIRE_PASSWORD_REUSE_PREVENTION` | `true` |
| `ADMIN_PORTS` | `22,3389` |
| `ALERT_ON_NON_COMPLIANT` | `true` |

## Step 6 — EventBridge Schedule

Use:

```text
eventbridge/schedule.json
```

Recommended:

```text
rate(6 hours)
```

## Step 7 — Security Event Rule

Use:

```text
eventbridge/security-events.json
```

It matches selected events such as:

- Root account use
- Console login failures
- IAM policy changes
- Security Group changes
- CloudTrail changes
- KMS key disable or scheduled deletion

## Checklist

- [ ] SNS topic created
- [ ] Subscription confirmed
- [ ] Report bucket created
- [ ] Lambda role created
- [ ] Lambda created
- [ ] Environment variables configured
- [ ] Scheduled rule created
- [ ] Security event rule created
