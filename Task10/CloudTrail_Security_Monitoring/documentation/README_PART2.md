# Part 2 — CloudTrail, SNS and Notification Setup

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Verify CloudTrail

Open:

```text
CloudTrail → Event history
```

Confirm management events are visible.

For retention, create a trail:

```text
Trail name: task10-security-trail
Management events: Read and Write
Global service events: Enabled
Log file validation: Enabled
```

IAM events are global-service management events.

## Step 2 — Create SNS Topic

```text
SNS Topic Name: task10-security-alerts
Type: Standard
```

Add an email subscription and confirm it.

Copy the Topic ARN:

```text
arn:aws:sns:<REGION>:<ACCOUNT_ID>:task10-security-alerts
```

## Step 3 — Optional Slack Integration

You may subscribe an HTTPS endpoint through another integration or let Lambda post directly to Slack.

The supplied Lambda supports:

```text
SLACK_SECRET_ID
```

Store the Slack webhook in Secrets Manager as:

```json
{
  "webhook_url": "https://hooks.slack.com/services/..."
}
```

## Step 4 — Notification Strategy

The Lambda always logs every matching event.

It publishes to SNS when:

```text
ENABLE_SNS=true
```

It posts to Slack when:

```text
ENABLE_SLACK=true
```

## Step 5 — Recommended Alert Details

- Event name
- Severity
- Actor ARN
- Account ID
- Region
- Source IP
- Event time
- Request parameters
- CloudTrail Event ID
- Lambda Request ID

## Checklist

- [ ] CloudTrail verified
- [ ] SNS topic created
- [ ] Subscription confirmed
- [ ] Optional Slack secret created
- [ ] Topic ARN recorded
