# Part 4 — EventBridge Rule, Testing and Verification

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Step 1 — Create the EventBridge Rule

Open:

```text
Amazon EventBridge → Rules → Create rule
```

Configure:

```text
Name: task9-detect-iam-user-creation
Event bus: default
Rule type: Rule with an event pattern
```

Use the supplied pattern:

```text
eventbridge/event-pattern.json
```

Pattern:

```json
{
  "source": ["aws.iam"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["iam.amazonaws.com"],
    "eventName": ["CreateUser"]
  }
}
```

## Step 2 — Configure Lambda as Target

Choose:

```text
Target type: AWS service
Target: Lambda function
Function: task9-unauthorized-iam-user-alert
```

EventBridge adds permission to invoke Lambda.

## Step 3 — Controlled End-to-End Test

In a test account or approved environment:

```bash
aws iam create-user \
  --user-name task9-security-test-user
```

Expected flow:

```text
CreateUser API call
→ CloudTrail event
→ EventBridge match
→ Lambda invocation
→ Slack alert
→ CloudWatch log
```

## Step 4 — Verify Slack Alert

The Slack message should contain:

```text
Unauthorized IAM User Created
New user: task9-security-test-user
Created by: <CREATOR_ARN>
Source IP: <IP>
Event time: <UTC_TIME>
Event ID: <CLOUDTRAIL_EVENT_ID>
```

## Step 5 — Verify CloudWatch Logs

Open:

```text
CloudWatch → Log groups
→ /aws/lambda/task9-unauthorized-iam-user-alert
```

Expected log fields:

- Event ID
- New username
- Creator ARN
- Authorization result
- Slack HTTP status
- Request ID

## Step 6 — Delete the Test User

```bash
aws iam delete-user \
  --user-name task9-security-test-user
```

Delete attached resources first if the user has policies, groups, login profile, MFA devices or access keys.

## Step 7 — Verify Authorized-Creator Behavior

Add your approved admin ARN to:

```text
AUTHORIZED_CREATOR_ARNS
```

Create another controlled test user.

Expected:

```text
Lambda logs authorized creation
No Slack alert when ALERT_ON_AUTHORIZED=false
```

## Optional CloudWatch Alarms

Create alarms for:

```text
Lambda Errors >= 1
Lambda Throttles >= 1
Lambda Duration >= 12000 ms
```

## Checklist

- [ ] EventBridge rule created
- [ ] Correct event pattern used
- [ ] Lambda configured as target
- [ ] Unauthorized test performed
- [ ] Slack alert received
- [ ] CloudWatch logs verified
- [ ] Test user deleted
- [ ] Authorized behavior verified
