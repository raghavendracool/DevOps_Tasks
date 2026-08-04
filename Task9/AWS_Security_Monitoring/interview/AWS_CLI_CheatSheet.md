# Task 9 — AWS CLI Cheat Sheet

## Create Test User

```bash
aws iam create-user \
  --user-name task9-security-test-user
```

## Delete Test User

```bash
aws iam delete-user \
  --user-name task9-security-test-user
```

## Search CloudTrail Event History

```bash
aws cloudtrail lookup-events \
  --lookup-attributes \
    AttributeKey=EventName,AttributeValue=CreateUser
```

## Test EventBridge Pattern

```bash
aws events test-event-pattern \
  --event-pattern file://eventbridge/event-pattern.json \
  --event file://lambda/test-event.json
```

## Invoke Lambda

```bash
aws lambda invoke \
  --function-name task9-unauthorized-iam-user-alert \
  --payload fileb://lambda/test-event.json \
  response.json
```

## Tail Logs

```bash
aws logs tail \
  /aws/lambda/task9-unauthorized-iam-user-alert \
  --follow
```

## Read Secret Metadata

```bash
aws secretsmanager describe-secret \
  --secret-id task9/slack-webhook-url
```

Do not print the secret value in shared terminals or logs.
