# Task 10 — Troubleshooting Guide

## Detection Path

```text
API call
  ↓
CloudTrail event exists?
  ↓
EventBridge pattern matches?
  ↓
Lambda invocation occurs?
  ↓
CloudWatch log written?
  ↓
SNS/Slack delivery successful?
```

## Common Root Causes

- Incorrect event source
- Wrong event detail type
- Rule created in wrong region
- Missing Lambda invoke permission
- SNS subscription pending
- Secret ARN mismatch
- S3 region filter missing
- Lambda inside VPC without internet path

## Production Improvements

- EventBridge DLQ
- Lambda failure destination
- DynamoDB deduplication
- Security Hub integration
- Centralized multi-account monitoring
- SIEM forwarding
- Automated ticket creation
