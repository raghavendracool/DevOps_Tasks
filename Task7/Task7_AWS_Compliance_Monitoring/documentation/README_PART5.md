# Part 5 — Verification, Cleanup and Troubleshooting

[← Part 4](README_PART4.md) | [Main README](../README.md)

## End-to-End Verification

Verify Lambda configuration:

```bash
aws lambda get-function-configuration \
  --function-name task7-compliance-monitor
```

Confirm:

```text
Timeout: 30
```

Invoke:

```bash
aws lambda invoke \
  --function-name task7-compliance-monitor \
  --payload '{"source":"manual-cli-test"}' \
  response.json
```

View:

```bash
cat response.json
```

Tail logs:

```bash
aws logs tail \
  /aws/lambda/task7-compliance-monitor \
  --follow
```

## Expected Report Structure

```json
{
  "compliance_status": "NON_COMPLIANT",
  "summary": {
    "ec2_missing_required_tags": 1,
    "ebs_unencrypted": 1,
    "iam_access_keys_over_age": 1,
    "total_non_compliant": 3
  },
  "findings": []
}
```

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| EC2 results empty | Wrong region | `SCAN_REGIONS` |
| Lambda times out | Too many regions/resources | Duration and region count |
| IAM access denied | Missing global IAM permissions | Execution role |
| SNS not received | Subscription unconfirmed | SNS subscriptions |
| EBS result wrong | Wrong region or pagination | Logs and API output |
| Tags appear missing | Tag key case mismatch | Required tag values |
| Duplicate emails | Overlapping executions | Reserved concurrency |
| Partial report | Remaining-time protection | `partial_scan` field |

## Important Design Limitations

### Thirty-Second Timeout

A large multi-region account may not complete within 30 seconds.

Production alternatives:

- AWS Config managed rules
- AWS Config custom Lambda rules
- Step Functions Map workflow
- SQS-based regional workers
- AWS Organizations delegated administrator
- Security Hub findings
- Systems Manager Automation remediation

### Access-Key Rotation

The monitor detects old keys but does not rotate them automatically.

Safe rotation requires:

1. Create new key.
2. Update applications and secrets.
3. Validate usage.
4. Disable old key.
5. Delete old key after confirmation.

## Cleanup

1. Disable and delete EventBridge schedule.
2. Delete CloudWatch alarms.
3. Delete Lambda function.
4. Delete custom IAM policy.
5. Delete execution role.
6. Delete SNS subscription and topic.
7. Delete CloudWatch Log Group if not required.
8. Restore any tags or test settings changed.

## Final Checklist

- [ ] Lambda timeout is 30 seconds
- [ ] EC2 tag violations detected
- [ ] Unencrypted EBS volumes detected
- [ ] Keys older than two days detected
- [ ] CloudWatch logs generated
- [ ] SNS notification received
- [ ] EventBridge scheduled scan verified
- [ ] Production limitations understood
