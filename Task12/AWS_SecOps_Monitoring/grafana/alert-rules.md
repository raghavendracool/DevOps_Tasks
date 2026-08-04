# Grafana Alert Rules

## Rule 1 — Compliance Violation

- Data source: CloudWatch
- Namespace: `SecOps/Compliance`
- Metric: `NonCompliantControls`
- Statistic: Maximum
- Condition: `last() >= 1`
- Evaluation interval: 5 minutes
- Pending period: 5 minutes
- Severity label: `warning`

## Rule 2 — Critical Finding

- Metric: `CriticalFindings`
- Statistic: Maximum
- Condition: `last() >= 1`
- Evaluation interval: 1 minute
- Pending period: 0 minutes
- Severity label: `critical`

## Rule 3 — Unauthorized Activity

- Metric: `UnauthorizedActivities`
- Statistic: Sum
- Range: 5 minutes
- Condition: `sum() >= 1`
- Evaluation interval: 1 minute
- Severity label: `critical`

## Rule 4 — Compliance Score Degradation

- Metric: `ComplianceScore`
- Statistic: Average
- Condition: `last() < 100`
- Evaluation interval: 5 minutes
- Pending period: 10 minutes
- Severity label: `warning`

## Contact Point Test

Use Grafana:

```text
Alerting → Contact points → Test
```

Confirm successful delivery before enabling production alert rules.
