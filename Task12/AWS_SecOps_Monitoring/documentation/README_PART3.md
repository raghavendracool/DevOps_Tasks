# Part 3 — Compliance Checks and Custom Metrics

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Lambda Source

```text
lambda/lambda_function.py
```

## Metric Design

The Lambda publishes custom metrics using CloudWatch `PutMetricData`. CloudWatch supports custom namespaces, metric names and dimensions for application-defined measurements. citeturn347411search11turn347411search18turn347411search40

### Summary Metrics

| Metric | Meaning |
|---|---|
| `ComplianceScore` | Percentage of checks that passed |
| `TotalControlsEvaluated` | Number of checks evaluated |
| `NonCompliantControls` | Count of failed checks |
| `CriticalFindings` | Critical findings count |
| `UnauthorizedActivities` | Security events count |
| `PartialScan` | `1` when scan stopped early |

### Per-Control Metric

```text
Metric: ControlNonCompliant
Dimensions:
- ControlId
- Severity
```

### Per-Region Metric

```text
Metric: RegionNonCompliantResources
Dimension:
- Region
```

## Compliance Score

```text
Compliance Score =
(Passed controls / Total evaluated controls) × 100
```

## Event-Driven Metric

When Lambda receives a CloudTrail event from EventBridge, it publishes:

```text
UnauthorizedActivities = 1
```

with dimensions:

```text
EventName
Severity
```

## Report Storage

Each scheduled run stores a JSON report:

```text
s3://<REPORT_BUCKET>/compliance-reports/YYYY/MM/DD/<request-id>.json
```

## Structured Log Example

```json
{
  "compliance_score": 75.0,
  "total_controls": 8,
  "non_compliant_controls": 2,
  "critical_findings": 1,
  "findings": []
}
```

## Recommended CloudWatch Alarms

### Any Non-Compliance

```text
Metric: NonCompliantControls
Threshold: >= 1
```

### Critical Findings

```text
Metric: CriticalFindings
Threshold: >= 1
```

### Unauthorized Activity

```text
Metric: UnauthorizedActivities
Threshold: >= 1
```

### Compliance Score

```text
Metric: ComplianceScore
Threshold: < 100
```

## Checklist

- [ ] Lambda deployed
- [ ] Metrics appear in `SecOps/Compliance`
- [ ] S3 report created
- [ ] CloudWatch logs contain structured report
- [ ] CloudWatch alarms configured
