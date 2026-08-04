# Part 3 — Compliance Lambda Code and Rules

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Lambda Source

The supplied file is:

```text
lambda/lambda_function.py
```

## Check 1 — EC2 Required Tags

The function lists EC2 instances in every configured region.

An instance is non-compliant when any required tag:

- Is missing
- Exists with an empty value

Example violation:

```json
{
  "resource_type": "EC2_INSTANCE",
  "resource_id": "i-0123456789abcdef0",
  "region": "ap-south-1",
  "rule": "REQUIRED_TAGS",
  "missing_tags": ["Owner", "CostCenter"]
}
```

Stopped instances are still checked because the requirement says no EC2 instance should exist without tags.

Terminated instances are not returned as active resources.

## Check 2 — EBS Encryption

The function calls `DescribeVolumes`.

A volume is non-compliant when:

```python
volume.get("Encrypted", False) is False
```

Example:

```json
{
  "resource_type": "EBS_VOLUME",
  "resource_id": "vol-0123456789abcdef0",
  "region": "ap-south-1",
  "rule": "EBS_ENCRYPTION",
  "state": "available"
}
```

## Check 3 — IAM Access-Key Rotation

The function:

1. Lists IAM users.
2. Lists access keys for each user.
3. Evaluates active keys.
4. Compares `CreateDate` with the current UTC time.
5. Reports keys older than two days.

Example:

```json
{
  "resource_type": "IAM_ACCESS_KEY",
  "resource_id": "AKIA...REDACTED",
  "user_name": "application-user",
  "rule": "ACCESS_KEY_ROTATION",
  "age_days": 8,
  "maximum_days": 2
}
```

The function masks most of the key ID in notifications.

## Check 4 — Logging and Notification

Every run writes one structured JSON report to CloudWatch.

SNS notification occurs when:

```text
total_non_compliant > 0
```

Optional compliant-run notifications can be enabled using:

```text
NOTIFY_ON_COMPLIANT=true
```

## Pagination

The implementation uses paginators for:

- `DescribeInstances`
- `DescribeVolumes`
- `ListUsers`
- `ListAccessKeys`

This is necessary for accounts with many resources.

## 30-Second Runtime Protection

Before each major operation, the function checks Lambda remaining time.

If less than the configured safety threshold remains, it stops safely and reports a partial scan.

## Deployment

Paste the supplied code into the Lambda editor and select:

```text
Deploy
```

Or package it:

```bash
cd lambda
zip compliance-monitor.zip lambda_function.py
```

## Checklist

- [ ] Source code deployed
- [ ] Paginators used
- [ ] Required tags configured
- [ ] Two-day access-key age configured
- [ ] SNS ARN configured
- [ ] Code handles remaining time
