# Task 12 — AWS CLI Cheat Sheet

## Invoke Lambda

```bash
aws lambda invoke \
  --function-name task12-secops-compliance-engine \
  --payload '{"source":"manual-compliance-scan"}' \
  response.json
```

## List Metrics

```bash
aws cloudwatch list-metrics \
  --namespace SecOps/Compliance
```

## Get Compliance Score

```bash
aws cloudwatch get-metric-statistics \
  --namespace SecOps/Compliance \
  --metric-name ComplianceScore \
  --statistics Average \
  --period 300 \
  --start-time "$(date -u -d '1 hour ago' +%FT%TZ)" \
  --end-time "$(date -u +%FT%TZ)"
```

## Tail Logs

```bash
aws logs tail \
  /aws/lambda/task12-secops-compliance-engine \
  --follow
```

## List Reports

```bash
aws s3 ls \
  s3://<REPORT_BUCKET>/compliance-reports/ \
  --recursive
```

## Check Security Hub Standards

```bash
aws securityhub get-enabled-standards
```

## Check Config Recorders

```bash
aws configservice describe-configuration-recorder-status
```
