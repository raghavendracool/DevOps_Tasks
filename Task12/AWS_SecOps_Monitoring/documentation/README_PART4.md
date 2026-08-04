# Part 4 — Grafana Dashboard and Alerting

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Option A — Amazon Managed Grafana

Create:

```text
Workspace name: task12-secops-grafana
Authentication: AWS IAM Identity Center or SAML
Permission type: Service managed
```

Amazon Managed Grafana can connect to Amazon CloudWatch as a native data source. citeturn347411search4turn347411search24turn347411search30

## CloudWatch Data-Source Permissions

The Grafana workspace role needs read permissions such as:

```text
cloudwatch:DescribeAlarmsForMetric
cloudwatch:DescribeAlarmHistory
cloudwatch:DescribeAlarms
cloudwatch:ListMetrics
cloudwatch:GetMetricData
cloudwatch:GetInsightRuleReport
logs:DescribeLogGroups
logs:GetLogGroupFields
logs:StartQuery
logs:StopQuery
logs:GetQueryResults
ec2:DescribeTags
```

Use:

```text
iam/grafana-cloudwatch-policy.json
```

## Import Dashboard

Import:

```text
grafana/secops-dashboard.json
```

Panels include:

- Compliance Score
- Non-Compliant Controls
- Critical Findings
- Unauthorized Activities
- Control failures by control ID
- Findings by Region
- Lambda errors and duration

## Grafana Alerting

Amazon Managed Grafana supports centralized Grafana alerting and CloudWatch as an alert-capable data source. citeturn347411search10turn347411search17turn347411search38

Create alert rules:

### Compliance Violation

```text
Query: NonCompliantControls
Condition: Last value >= 1
Evaluation: Every 5 minutes
For: 5 minutes
Severity: Warning
```

### Critical Security Finding

```text
Query: CriticalFindings
Condition: Last value >= 1
Evaluation: Every 1 minute
For: 0 minutes
Severity: Critical
```

### Unauthorized Activity

```text
Query: UnauthorizedActivities
Condition: Sum over 5 minutes >= 1
Severity: Critical
```

## Contact Points

Configure:

- Email
- Slack
- Microsoft Teams
- PagerDuty
- Webhook

## Dashboard Verification

1. Run Lambda manually.
2. Open CloudWatch custom metrics.
3. Confirm data is present.
4. Open Grafana dashboard.
5. Select the correct AWS Region.
6. Trigger a controlled violation.
7. Confirm panel update.
8. Confirm alert delivery.

## Checklist

- [ ] Grafana workspace created
- [ ] CloudWatch data source added
- [ ] Dashboard JSON imported
- [ ] Metrics visible
- [ ] Alert rules configured
- [ ] Contact point tested
