# Task 12 — Interview Guide

## 1. Explain the architecture.

EventBridge invokes Lambda on a schedule and for selected CloudTrail events. Lambda evaluates compliance, publishes custom CloudWatch metrics, stores JSON reports, and sends notifications. Grafana reads CloudWatch and displays dashboards and alerts.

## 2. Why publish custom metrics?

They convert compliance results into time-series data that can be graphed, alarmed and trended.

## 3. Why use a custom namespace?

It separates project metrics from AWS service namespaces.

## 4. What is the difference between a finding and a metric?

A finding contains detailed evidence. A metric is an aggregated numeric measurement.

## 5. Why use Grafana if CloudWatch dashboards exist?

Grafana offers flexible visualization, multiple data sources, reusable dashboards and centralized alerting.

## 6. Why is this not full CIS certification?

A full assessment requires the approved benchmark version, all applicable controls, evidence, exceptions and audit validation.

## 7. Why use AWS Security Hub CSPM?

It provides managed security standards and centralized findings.

## 8. Why use AWS Config?

It records resource configuration and supports managed or custom compliance rules.

## 9. How do you handle multi-region scanning?

Use pagination and regional clients, or fan out work to regional workers.

## 10. How do you handle many accounts?

Use Organizations, delegated administration, Config aggregators and cross-account observability.

## 11. What is compliance score?

Passed controls divided by total evaluated controls, multiplied by 100.

## 12. How do you avoid metric explosion?

Limit high-cardinality dimensions and publish summary metrics.

## 13. How do you detect unauthorized activity?

Use EventBridge rules matching CloudTrail events and publish an event metric.

## 14. How do you avoid duplicate incidents?

Deduplicate using CloudTrail event ID in DynamoDB.

## 15. How do you secure Grafana?

Use IAM Identity Center or SAML, least privilege, private connectivity where needed and restricted workspace roles.

## 16. How do you test Grafana alerts?

Generate a controlled metric breach and use contact-point testing.

## 17. What happens if Lambda times out?

The report may be incomplete. Use partial-scan metrics and redesign with Step Functions or SQS.

## 18. Why archive reports in S3?

For historical evidence, audit review and trend analysis.

## 19. How do you automate remediation?

Separate detection and remediation, use approval workflows and maintain rollback.

## 20. How do you keep mappings current?

Version control control mappings and review them whenever CIS or AWS standards change.
