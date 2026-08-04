# Part 1 — Introduction, Architecture and Scope

[← Main README](../README.md) | [Next: Part 2 →](README_PART2.md)

## Objective

Build an AWS SecOps solution that:

- Runs recurring compliance checks
- Detects non-compliant resources
- Detects selected unauthorized activities
- Publishes custom CloudWatch metrics
- Displays those metrics in Grafana
- Sends alerts for compliance or security incidents

## Architecture

![Task 12 Architecture](../infographic.png)

## AWS Services Used

| Service | Purpose |
|---|---|
| AWS Lambda | Compliance engine and event processor |
| Amazon EventBridge | Scheduled and event-driven invocation |
| Amazon CloudWatch | Custom metrics, logs and alarms |
| Amazon Managed Grafana | Dashboards and alert visualization |
| Amazon SNS | Email or webhook notification |
| Amazon S3 | Compliance report archive |
| AWS Config | Recommended resource inventory and managed rules |
| AWS CloudTrail | Security activity source |
| IAM Access Analyzer | Recommended external-access findings |
| AWS Security Hub CSPM | Recommended managed compliance standard |

## Implemented Training Checks

| Check ID | Check |
|---|---|
| `IAM_ROOT_MFA` | Root account MFA is enabled |
| `IAM_PASSWORD_POLICY` | IAM password policy meets configured baseline |
| `IAM_OLD_ACCESS_KEYS` | Active access keys do not exceed configured age |
| `CLOUDTRAIL_MULTI_REGION` | At least one multi-region trail exists |
| `CLOUDTRAIL_LOG_VALIDATION` | Trail log-file validation is enabled |
| `CONFIG_RECORDER` | AWS Config recorder exists and is recording |
| `S3_PUBLIC_ACCESS_BLOCK` | Account-level S3 public access block is enabled |
| `SECURITY_GROUP_ADMIN_PORTS` | No unrestricted ingress to SSH or RDP |
| `UNAUTHORIZED_ACTIVITY` | Selected CloudTrail security events are counted |

## Important Version Note

The assignment specifies CIS AWS Foundations Benchmark `v1.7`. Current CIS and AWS-managed benchmark versions may differ. This package therefore keeps control IDs internal and documents each API check clearly so the implementation can be remapped to the benchmark version approved by your organization.

AWS Security Hub CSPM currently supports several CIS AWS Foundations standards, and CIS continues to publish newer benchmark versions. Use the approved benchmark document and Security Hub standard for formal compliance assessment. citeturn347411search0turn347411search2turn347411search22

## Metrics Namespace

```text
SecOps/Compliance
```

## Recommended Schedule

```text
rate(6 hours)
```

For a training demo:

```text
rate(15 minutes)
```

## Naming Convention

| Resource | Name |
|---|---|
| Lambda | `task12-secops-compliance-engine` |
| SNS topic | `task12-secops-alerts` |
| Report bucket | `task12-secops-reports-<unique>` |
| Schedule rule | `task12-compliance-schedule` |
| Security event rule | `task12-security-events` |
| Grafana workspace | `task12-secops-grafana` |

## Checklist

- [ ] AWS Region selected
- [ ] Approved control scope reviewed
- [ ] Metrics namespace understood
- [ ] SNS email or contact point available
- [ ] Report bucket name prepared
