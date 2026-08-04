# Part 5 — Cleanup, Troubleshooting and Production Improvements

[← Part 4](README_PART4.md) | [Main README](../README.md)

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| Lambda not invoked | Event pattern mismatch | EventBridge rule |
| Slack alert missing | Invalid webhook | Secret value |
| Secret access denied | IAM policy | Secret ARN |
| Authorized user alerted | ARN mismatch | STS vs IAM ARN |
| No creator ARN | Service identity | `userIdentity` fields |
| Duplicate alerts | Duplicate event delivery | Event ID deduplication |
| Slack 4xx/5xx | Payload/webhook issue | Lambda logs |
| Event delayed | CloudTrail/EventBridge latency | Event timestamps |

## Common Issue — Assumed Role ARN

IAM creator may appear as:

```text
arn:aws:sts::<ACCOUNT_ID>:assumed-role/security-admin/session-name
```

Allow-list this pattern:

```text
arn:aws:sts::<ACCOUNT_ID>:assumed-role/security-admin/*
```

## Common Issue — Slack Returns 404

The webhook may be revoked or copied incorrectly.

Update the secret with a new webhook URL.

## Common Issue — Lambda Cannot Access the Internet

A Lambda function outside a VPC has internet access by default.

If placed inside private VPC subnets, it needs:

- NAT Gateway for Slack
- Secrets Manager interface VPC endpoint
- Correct route tables and Security Groups

## Production Improvements

- Send findings to Security Hub
- Add SNS/SQS fallback if Slack fails
- Store processed event IDs in DynamoDB
- Add automated ticket creation
- Detect additional IAM events:
  - `CreateAccessKey`
  - `AttachUserPolicy`
  - `PutUserPolicy`
  - `CreateLoginProfile`
  - `DeactivateMFADevice`
- Add account and environment allow lists
- Add severity classification
- Encrypt secrets with a customer-managed KMS key
- Use AWS Organizations for central monitoring
- Add CloudTrail Lake for investigation

## Cleanup

1. Delete EventBridge rule.
2. Remove Lambda target permission if required.
3. Delete Lambda function.
4. Delete IAM execution role and policy.
5. Delete Secrets Manager secret.
6. Delete test IAM user.
7. Delete optional CloudWatch alarms.
8. Delete CloudTrail trail and S3 logs only when approved.
9. Remove Slack webhook integration if no longer needed.

## Final Verification

- [ ] Unauthorized creation generates Slack alert
- [ ] Alert contains required details
- [ ] CloudWatch records successful delivery
- [ ] Authorized creator does not alert
- [ ] Test IAM users are removed
- [ ] Secret remains private
