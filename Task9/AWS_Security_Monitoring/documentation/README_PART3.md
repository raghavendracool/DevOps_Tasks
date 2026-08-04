# Part 3 — Lambda Function and IAM Permissions

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Step 1 — Create the Lambda Function

Configure:

```text
Function name: task9-unauthorized-iam-user-alert
Runtime: Python 3.12
Architecture: x86_64
Memory: 128 MB
Timeout: 15 seconds
```

## Step 2 — Create the Lambda Execution Role

Create:

```text
Role name: task9-security-monitor-role
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

Replace:

```text
<REGION>
<ACCOUNT_ID>
<SECRET_SUFFIX>
```

## Step 3 — Configure Environment Variables

| Variable | Example |
|---|---|
| `SLACK_SECRET_ID` | `task9/slack-webhook-url` |
| `AUTHORIZED_CREATOR_ARNS` | Comma-separated IAM ARNs |
| `ALERT_ON_AUTHORIZED` | `false` |
| `SLACK_CHANNEL_NAME` | `#aws-security-alerts` |

## Step 4 — Deploy the Lambda Code

Use:

```text
lambda/lambda_function.py
```

The function:

1. Extracts CloudTrail details from the EventBridge event.
2. Extracts the new IAM username.
3. Identifies the creator ARN.
4. Compares the creator with the allow list.
5. Skips alerts for authorized creators unless configured otherwise.
6. Retrieves the Slack webhook from Secrets Manager.
7. Sends a Slack Block Kit message.
8. Logs Slack delivery status.
9. Raises an exception if Slack rejects the message.

## Authorization Logic

The creator ARN may appear as:

```text
detail.userIdentity.arn
```

For assumed roles, the ARN can be an STS session ARN.

The supplied implementation supports exact ARNs and prefix-style values ending with `*`.

Example:

```text
arn:aws:sts::<ACCOUNT_ID>:assumed-role/security-admin/*
```

## Step 5 — Test with a Sample Event

Use:

```text
lambda/test-event.json
```

Update the account ID and ARNs before testing.

## Checklist

- [ ] Lambda created
- [ ] Timeout configured
- [ ] IAM role attached
- [ ] Secret permission restricted
- [ ] Environment variables added
- [ ] Lambda code deployed
- [ ] Sample event updated
