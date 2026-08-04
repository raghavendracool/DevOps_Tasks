# Part 5 — Testing, Troubleshooting, Cleanup and Production Recommendations

[← Part 4](README_PART4.md) | [Main README](../README.md)

## Manual Test

```bash
aws lambda invoke \
  --function-name task12-secops-compliance-engine \
  --payload '{"source":"manual-compliance-scan"}' \
  response.json
```

## Controlled Violations

Use only in a sandbox:

- Temporarily remove account-level S3 Public Access Block
- Create a Security Group rule allowing SSH from `0.0.0.0/0`
- Disable AWS Config recorder
- Use a test IAM key older than the configured threshold where available

Restore immediately after testing.

## Verification

```bash
aws cloudwatch list-metrics \
  --namespace SecOps/Compliance

aws logs tail \
  /aws/lambda/task12-secops-compliance-engine \
  --follow

aws s3 ls \
  s3://<REPORT_BUCKET>/compliance-reports/ \
  --recursive
```

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| No metrics | Missing `PutMetricData` | Lambda IAM role |
| Grafana blank | Wrong region/namespace | Dashboard variables |
| Alert not firing | No data or wrong reducer | Grafana rule |
| Partial scan | Lambda timeout | Regions and pagination |
| S3 report missing | PutObject denied | Bucket ARN |
| Root MFA check fails | Credential report stale | Generate report |
| Config check fails | Recorder not configured | AWS Config |
| SG false positive | IPv6 or port range | Rule logic |

## Production Recommendations

### Prefer Managed Compliance

For formal compliance, enable Security Hub CSPM and AWS Config in all required Regions. Security Hub uses AWS Config for many controls and supports managed CIS standards. citeturn347411search0turn347411search20

### Use Current Approved Benchmark

CIS publishes newer AWS Foundations benchmark versions. Keep mappings version-controlled and reviewed by security governance. citeturn347411search2turn347411search22

### Multi-Account Design

- AWS Organizations
- Security Hub delegated administrator
- Config aggregator
- CloudWatch cross-account observability
- Central Amazon Managed Grafana workspace

Amazon Managed Grafana can work with CloudWatch across accounts when cross-account observability and required permissions are configured. citeturn347411search31

### Reliability

- SQS between event sources and Lambda
- Dead-letter queues
- DynamoDB deduplication
- Step Functions for large scans
- Reserved concurrency
- Alarms on Lambda Errors and Duration

### Evidence

- Store immutable reports in S3
- Enable Object Lock where required
- Retain CloudTrail logs
- Record remediation tickets
- Document exceptions and risk acceptance

## Cleanup

1. Delete EventBridge rules.
2. Delete Grafana alert rules and workspace if not needed.
3. Delete CloudWatch alarms.
4. Delete Lambda function.
5. Delete IAM roles and policies.
6. Delete SNS topic.
7. Empty and delete report bucket.
8. Delete optional Config rules only after approval.
9. Retain evidence according to policy.
