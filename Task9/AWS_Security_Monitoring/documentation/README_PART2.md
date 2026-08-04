# Part 2 — CloudTrail, Slack Webhook and Secrets Manager

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Verify CloudTrail

CloudTrail Event History records recent management events by default.

For long-term retention, create a trail:

```text
CloudTrail → Trails → Create trail
```

Recommended:

```text
Trail name: task9-security-trail
Management events: Read and Write
Include global service events: Enabled
S3 log validation: Enabled
```

IAM is a global service, but CloudTrail records the API event with event details that EventBridge can match.

## Step 2 — Create a Slack Incoming Webhook

In Slack:

1. Create or select a security-alerts channel.
2. Add an Incoming Webhook integration.
3. Select the destination channel.
4. Copy the webhook URL.

Example format:

```text
https://hooks.slack.com/services/...
```

Do not commit this URL to GitHub.

## Step 3 — Store the Webhook in Secrets Manager

Open:

```text
AWS Secrets Manager → Store a new secret
```

Choose:

```text
Secret type: Other type of secret
Key: webhook_url
Value: <SLACK_WEBHOOK_URL>
Secret name: task9/slack-webhook-url
```

The sample Lambda supports either:

```json
{
  "webhook_url": "https://hooks.slack.com/services/..."
}
```

or a plain-text secret containing only the webhook URL.

## Step 4 — Record the Secret ARN

Example:

```text
arn:aws:secretsmanager:<REGION>:<ACCOUNT_ID>:secret:task9/slack-webhook-url-xxxxxx
```

## Step 5 — Security Best Practices

- Restrict `secretsmanager:GetSecretValue` to the exact secret ARN.
- Do not log the webhook URL.
- Enable secret rotation only if your Slack integration process supports it.
- Use CloudTrail to audit secret retrieval.
- Limit Lambda environment variables to non-secret configuration.

## Checklist

- [ ] CloudTrail management events verified
- [ ] Slack webhook created
- [ ] Webhook stored in Secrets Manager
- [ ] Secret ARN recorded
- [ ] Secret not committed to GitHub
