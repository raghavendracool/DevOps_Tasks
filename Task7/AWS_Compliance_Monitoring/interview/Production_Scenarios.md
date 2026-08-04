# Task 7 — Real-Time Production Scenarios

## Scenario 1 — Lambda Times Out at 30 Seconds

Check:

- Number of configured regions
- Number of resources
- API throttling
- CloudWatch Duration
- Remaining-time partial-scan flag

Solution:

- Scan fewer regions per invocation
- Fan out through SQS
- Use Step Functions
- Use AWS Config for continuous compliance

## Scenario 2 — An EC2 Instance Has All Tags but Is Reported Non-Compliant

Possible causes:

- Tag key case mismatch
- Empty tag value
- Leading or trailing spaces
- Different organization naming standard
- Stale report from previous invocation

## Scenario 3 — SNS Email Is Not Received

Check:

- Subscription confirmation
- Topic ARN environment variable
- `sns:Publish` permission
- Spam folder
- SNS delivery status
- CloudWatch error logs

## Scenario 4 — IAM Keys Older Than Two Days Are Not Detected

Check:

- Key is Active
- `iam:ListUsers` and `iam:ListAccessKeys`
- Pagination
- UTC time calculation
- Lambda role permissions

## Scenario 5 — Too Many Emails Are Sent

Implement stateful deduplication:

- Create a finding fingerprint
- Store current state in DynamoDB
- Notify only on new, changed or resolved findings
- Send scheduled summaries instead of every run

## Scenario 6 — Security Requests Automatic Key Rotation

Explain that key rotation is not only an IAM API operation.

The application using the credential must be updated and validated before the old key is disabled.

## Scenario 7 — An Unencrypted Production EBS Volume Is Found

Do not detach it immediately.

Create a change plan:

1. Snapshot volume.
2. Copy snapshot with encryption.
3. Create encrypted replacement volume.
4. Schedule downtime or failover.
5. Attach and validate.
6. Roll back when required.

## Scenario 8 — The Account Has 20 Regions

A single 30-second Lambda may not be sufficient.

Use one regional task per message through SQS or Step Functions Map.

## Scenario 9 — Compliance Must Cover 100 AWS Accounts

Use AWS Organizations, delegated administration, cross-account roles, Config aggregators and a central security account.

## Scenario 10 — API Throttling Occurs

Use SDK retries, exponential backoff, controlled concurrency and regional partitioning.

## Scenario 11 — A User Deletes a Required Tag After the Scan

The next scheduled run detects it. For near-real-time detection, use CloudTrail events through EventBridge in addition to scheduled scans.

## Scenario 12 — Compliance Team Needs Historical Trends

Store summarized reports in S3 or DynamoDB and create dashboards using Athena, QuickSight or CloudWatch.

## Scenario 13 — A Key Is Exactly Two Days Old

The code treats it as compliant until age is greater than two days. Confirm the business interpretation of the boundary.

## Scenario 14 — SNS Contains Too Much Data

Publish a summary and store the detailed report in S3, then include the S3 location in the notification.

## Scenario 15 — A Region Is Disabled

Handle `UnauthorizedOperation` or region-access errors, log them and mark the report partial.

## Scenario 16 — Lambda Has Broad `Resource: *`

Some read-only EC2 and IAM list APIs require `Resource: *`. Restrict actions and use permission boundaries, SCPs and a dedicated role.

## Scenario 17 — Compliance Requires Auto-Remediation

Separate detection and remediation. Require approvals for destructive changes and maintain rollback procedures.

## Scenario 18 — CloudWatch Shows Duration Near 30 Seconds

Create a Duration alarm around 25 seconds and reduce scope before hard timeouts begin.

## Scenario 19 — Unencrypted Volume Is Unattached

It is still non-compliant because the rule applies to all EBS volumes, not only attached volumes.

## Scenario 20 — Management Wants a Compliance Dashboard

Publish custom metrics or findings to Security Hub and visualize trends in CloudWatch or QuickSight.
