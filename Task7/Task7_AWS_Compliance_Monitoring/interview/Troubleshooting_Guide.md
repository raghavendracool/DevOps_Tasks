# Task 7 — Troubleshooting Guide

## No Findings Returned

```text
Correct regions configured?
        ↓
Execution role has Describe/List permissions?
        ↓
Paginators returning resources?
        ↓
Required tag keys match exact case?
        ↓
Check CloudWatch structured report
```

## Timeout

Emergency reduction:

```text
SCAN_REGIONS=ap-south-1
```

Then redesign for fan-out before adding regions.

## Access Denied

Check:

```text
Lambda execution role
Permission boundary
Organization SCP
SNS topic policy
KMS key policy
```

## SNS Failure

```bash
aws sns list-subscriptions-by-topic \
  --topic-arn <SNS_TOPIC_ARN>
```

Subscription must be `Confirmed`.

## Partial Scan

The report contains:

```json
"partial_scan": true
```

This means the function stopped because little execution time remained.

## Production Improvements

- AWS Config managed rules
- Security Hub custom findings
- EventBridge change-driven detection
- DynamoDB finding-state tracking
- SQS fan-out
- Step Functions orchestration
- Organizations multi-account support
- Automatic ticket creation
- Approval-controlled remediation
