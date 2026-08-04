# Part 2 — IAM Role, SNS Topic and Lambda Configuration

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Create the SNS Topic

Open:

```text
Amazon SNS → Topics → Create topic
```

Configure:

```text
Type: Standard
Name: task7-compliance-alerts
```

Create a subscription:

```text
Protocol: Email
Endpoint: your-email@example.com
```

Confirm the subscription from the email received.

Copy the Topic ARN:

```text
arn:aws:sns:<REGION>:<ACCOUNT_ID>:task7-compliance-alerts
```

## Step 2 — Create the Lambda Execution Role

Create:

```text
Role name: task7-compliance-lambda-role
Trusted entity: AWS Lambda
```

Attach the AWS-managed basic logging policy:

```text
AWSLambdaBasicExecutionRole
```

Add the supplied custom policy:

```text
lambda/iam-policy.json
```

Replace:

```text
<REGION>
<ACCOUNT_ID>
```

## Required Read Permissions

The function uses:

```text
ec2:DescribeInstances
ec2:DescribeVolumes
iam:ListUsers
iam:ListAccessKeys
sns:Publish
```

## Step 3 — Create the Lambda Function

Configure:

```text
Function name: task7-compliance-monitor
Runtime: Python 3.12
Architecture: x86_64
Execution role: task7-compliance-lambda-role
Memory: 256 MB
Timeout: 30 seconds
```

The timeout must be exactly:

```text
30 seconds
```

## Step 4 — Configure Environment Variables

| Variable | Example |
|---|---|
| `REQUIRED_TAGS` | `Environment,Owner,Project,CostCenter` |
| `MAX_ACCESS_KEY_AGE_DAYS` | `2` |
| `SCAN_REGIONS` | `ap-south-1` |
| `SNS_TOPIC_ARN` | SNS Topic ARN |
| `NOTIFY_ON_COMPLIANT` | `false` |

When SNS notifications are not required, leave `SNS_TOPIC_ARN` empty.

## Step 5 — Configure Reserved Concurrency

Optional lab setting:

```text
Reserved concurrency: 1
```

This prevents multiple overlapping account scans.

## Step 6 — Verify Lambda Settings

Check:

```text
Runtime: Python 3.12
Memory: 256 MB
Timeout: 0 min 30 sec
Role: task7-compliance-lambda-role
```

## Checklist

- [ ] SNS topic created
- [ ] Email subscription confirmed
- [ ] Lambda role created
- [ ] IAM policy attached
- [ ] Lambda created
- [ ] Timeout set to 30 seconds
- [ ] Environment variables configured
