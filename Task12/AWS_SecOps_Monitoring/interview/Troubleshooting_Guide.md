# Task 12 — Troubleshooting Guide

## No CloudWatch Metrics

```text
Lambda succeeded?
  ↓
cloudwatch:PutMetricData allowed?
  ↓
Namespace exactly SecOps/Compliance?
  ↓
Correct Region selected?
  ↓
Metric timestamp inside dashboard range?
```

## Grafana Access Denied

Check:

- Workspace role
- CloudWatch read policy
- AWS account and Region
- Data-source authentication
- Cross-account observability configuration

## Alert No Data

Choose an explicit no-data state:

- Alerting
- Normal
- Error
- Keep last state

## Lambda Errors

```bash
aws logs tail \
  /aws/lambda/task12-secops-compliance-engine \
  --since 30m
```

## Production Improvements

- Security Hub CSPM
- AWS Config managed rules
- Config aggregator
- CloudWatch cross-account observability
- Grafana contact-point fallback
- SQS and DLQ
- DynamoDB deduplication
- Immutable S3 evidence
