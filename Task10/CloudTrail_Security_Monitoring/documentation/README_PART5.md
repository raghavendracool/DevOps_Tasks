# Part 5 — Verification, Troubleshooting and Cleanup

[← Part 4](README_PART4.md) | [Main README](../README.md)

## Verification Commands

Tail logs:

```bash
aws logs tail \
  /aws/lambda/task10-cloudtrail-security-monitor \
  --follow
```

Search CloudTrail:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes \
    AttributeKey=EventName,AttributeValue=CreateAccessKey

aws cloudtrail lookup-events \
  --lookup-attributes \
    AttributeKey=EventName,AttributeValue=DeleteUser

aws cloudtrail lookup-events \
  --lookup-attributes \
    AttributeKey=EventName,AttributeValue=DeleteBucket
```

## Expected Log Record

```json
{
  "event_name": "DeleteBucket",
  "severity": "CRITICAL",
  "actor_arn": "arn:aws:iam::123456789012:user/admin",
  "region": "us-east-1",
  "source_ip": "203.0.113.10",
  "event_id": "example-event-id"
}
```

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| Lambda not invoked | Rule mismatch | EventBridge pattern |
| IAM event missing | Global-event handling | CloudTrail and rule region |
| S3 alert outside us-east-1 | Missing region condition | S3 event pattern |
| SNS not received | Subscription pending | SNS status |
| Slack failed | Secret/webhook issue | Lambda logs |
| Duplicate alert | At-least-once delivery | Event ID dedupe |
| Archive failed | S3 permissions | Bucket policy |
| AccessDenied | IAM role | Exact ARN |

## Cleanup

1. Delete test access key.
2. Delete test IAM users.
3. Delete test S3 bucket.
4. Delete EventBridge rules.
5. Delete Lambda function.
6. Delete IAM role and policy.
7. Delete SNS topic and subscription.
8. Delete optional Slack secret.
9. Delete optional archive bucket.
10. Retain CloudTrail logs according to policy.

## Production Improvements

- EventBridge dead-letter queue
- Lambda failure destination
- DynamoDB deduplication
- Security Hub custom findings
- SIEM forwarding
- Cross-account event bus
- Automated incident ticket
- GuardDuty and Config integration
- KMS encryption
- Runbook links in alerts
