# Task 10 — AWS CLI Cheat Sheet

## Search CloudTrail

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=CreateAccessKey

aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteUser

aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteBucket
```

## Test Event Pattern

```bash
aws events test-event-pattern \
  --event-pattern file://eventbridge/iam-security-events.json \
  --event file://lambda/test-create-access-key.json
```

## Invoke Lambda

```bash
aws lambda invoke \
  --function-name task10-cloudtrail-security-monitor \
  --payload fileb://lambda/test-delete-user.json \
  response.json
```

## Tail Logs

```bash
aws logs tail \
  /aws/lambda/task10-cloudtrail-security-monitor \
  --follow
```

## List EventBridge Targets

```bash
aws events list-targets-by-rule \
  --rule task10-iam-security-events
```
