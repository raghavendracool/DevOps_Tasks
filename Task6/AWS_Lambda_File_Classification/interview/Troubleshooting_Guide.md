# Task 6 — Troubleshooting Guide

## Lambda Not Invoked

```text
Upload file
  ↓
Correct bucket?
  ↓
Correct incoming/ prefix?
  ↓
S3 notification exists?
  ↓
Lambda resource permission exists?
  ↓
Check CloudWatch logs and metrics
```

## Access Denied

Check:

```text
Lambda execution role
Bucket Policy
KMS key policy
Object Lock
Exact bucket ARN
Exact prefix ARN
```

## Recursive Invocation

Emergency action:

1. Disable or remove S3 trigger.
2. Set Lambda reserved concurrency to `0` if necessary.
3. Correct trigger prefix.
4. Re-enable after validation.

## Logs

```bash
aws logs tail \
  /aws/lambda/task6-file-classifier \
  --since 30m
```

## Key Validation

```python
logger.info("bucket=%s key=%s", bucket, source_key)
```

## Production Recommendations

- SQS between S3 and Lambda for controlled retries
- Failure destination
- CloudWatch alarms
- S3 Versioning
- KMS encryption
- IaC deployment
- Unit tests
- Structured logs
- Idempotency strategy
