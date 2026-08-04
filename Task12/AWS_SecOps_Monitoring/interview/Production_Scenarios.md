# Task 12 — Real-Time Production Scenarios

## Scenario 1 — Grafana Shows No Data

Check metric namespace, Region, workspace role permissions, data-source setup and dashboard time range.

## Scenario 2 — Metrics Exist but Alerts Do Not Fire

Check reducer, threshold, evaluation interval, no-data behavior and contact point.

## Scenario 3 — Lambda Times Out

Reduce regions, split controls, use Step Functions or SQS fan-out and publish a partial-scan metric.

## Scenario 4 — Compliance Score Suddenly Drops

Identify the failing control dimension, review CloudTrail changes and validate whether the change was approved.

## Scenario 5 — Too Many Metrics Increase Cost

Reduce dimensions, use summary metrics and avoid per-resource metrics unless necessary.

## Scenario 6 — Root MFA Check Fails Incorrectly

Generate a fresh IAM credential report and verify the root account row.

## Scenario 7 — Security Group Rule Is a False Positive

Review protocol, port range, IPv4 and IPv6 CIDRs and approved exceptions.

## Scenario 8 — Unauthorized Activity Metric Is Duplicated

Deduplicate by CloudTrail event ID.

## Scenario 9 — A New CIS Version Is Released

Review differences, update mappings, test in sandbox and version the dashboard and code.

## Scenario 10 — Security Hub and Lambda Disagree

Compare control scope, Region coverage, resource recording and evaluation timing.

## Scenario 11 — Config Recorder Is Disabled

Alert immediately and investigate CloudTrail for who changed it.

## Scenario 12 — Grafana Contact Point Fails

Use test delivery, review endpoint credentials and add SNS or PagerDuty fallback.

## Scenario 13 — Multi-Account Metrics Are Missing

Configure CloudWatch cross-account observability and workspace IAM permissions.

## Scenario 14 — S3 Report Upload Fails

Check bucket policy, KMS permissions, object ARN and Region.

## Scenario 15 — Compliance Exception Is Approved

Store exception metadata and exclude it transparently without deleting the raw finding.

## Scenario 16 — CloudWatch PutMetricData Is Throttled

Batch metrics and retry with exponential backoff.

## Scenario 17 — Critical Finding Must Open a Ticket

Send Grafana or SNS webhook to the ITSM platform and include control ID and evidence location.

## Scenario 18 — Grafana Workspace Is Publicly Reachable

Review authentication, network access, organization roles and SSO configuration.

## Scenario 19 — Lambda Role Has Excessive Permissions

Separate read-only compliance APIs from remediation permissions.

## Scenario 20 — Audit Requires 12 Months of Evidence

Retain encrypted S3 reports with lifecycle transitions and immutable retention where required.
