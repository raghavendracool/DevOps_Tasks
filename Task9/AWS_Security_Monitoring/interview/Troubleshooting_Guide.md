# Task 9 — Troubleshooting Guide

## Detection Path

```text
IAM CreateUser
  ↓
CloudTrail event exists?
  ↓
EventBridge rule matched?
  ↓
Lambda invocation count increased?
  ↓
Secret retrieved?
  ↓
Slack HTTP 2xx?
```

## Check EventBridge Rule

```bash
aws events describe-rule \
  --name task9-detect-iam-user-creation
```

## Check Targets

```bash
aws events list-targets-by-rule \
  --rule task9-detect-iam-user-creation
```

## Check Lambda Permission

```bash
aws lambda get-policy \
  --function-name task9-unauthorized-iam-user-alert
```

## Check Logs

```bash
aws logs tail \
  /aws/lambda/task9-unauthorized-iam-user-alert \
  --since 30m
```

## Common Root Causes

- Wrong event bus
- Rule disabled
- Incorrect detail type
- Secret ARN mismatch
- Unconfirmed or revoked Slack integration
- Lambda inside VPC without NAT
- STS ARN not matching allow list
- EventBridge target permission missing

## Production Improvements

- EventBridge DLQ
- Lambda failure destination
- DynamoDB deduplication
- Security Hub integration
- Automated incident ticket
- Cross-account central monitoring
- Expanded IAM event coverage
