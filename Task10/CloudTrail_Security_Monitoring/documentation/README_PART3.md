# Part 3 — Lambda Code and IAM Permissions

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Step 1 — Create Lambda

Configure:

```text
Function name: task10-cloudtrail-security-monitor
Runtime: Python 3.12
Architecture: x86_64
Memory: 256 MB
Timeout: 30 seconds
```

## Step 2 — Attach IAM Role

Use:

```text
iam/lambda-policy.json
```

The Lambda needs:

- CloudWatch Logs permissions
- `sns:Publish`
- `secretsmanager:GetSecretValue` only when Slack is enabled
- Optional `s3:PutObject` for archive storage

## Step 3 — Environment Variables

| Variable | Example |
|---|---|
| `SNS_TOPIC_ARN` | SNS Topic ARN |
| `ENABLE_SNS` | `true` |
| `ENABLE_SLACK` | `false` |
| `SLACK_SECRET_ID` | `task10/slack-webhook-url` |
| `ARCHIVE_BUCKET_NAME` | Optional log archive bucket |
| `ARCHIVE_PREFIX` | `security-events/` |

## Step 4 — Deploy Code

Use:

```text
lambda/lambda_function.py
```

The function:

1. Validates the CloudTrail event.
2. Determines event type.
3. Applies region validation for S3 `DeleteBucket`.
4. Assigns severity.
5. Extracts actor, source IP, account and request details.
6. Writes structured JSON to CloudWatch.
7. Publishes SNS notification.
8. Optionally sends Slack notification.
9. Optionally archives the event in S3.

## Event Severity

| Event | Severity |
|---|---|
| `CreateAccessKey` | High |
| `DeleteUser` | High |
| `DeleteBucket` | Critical |

## Step 5 — Manual Lambda Test

Use the supplied events:

```text
lambda/test-create-access-key.json
lambda/test-delete-user.json
lambda/test-delete-bucket.json
```

## Checklist

- [ ] Lambda created
- [ ] IAM role attached
- [ ] Environment variables configured
- [ ] Source deployed
- [ ] Test events updated
- [ ] All three tests successful
