# Task 6 — Real-Time Production Scenarios

## Scenario 1 — Lambda Is Not Triggered

Check:

1. S3 Event Notification exists.
2. Bucket and Lambda are in compatible Regions.
3. Lambda resource policy permits S3 invocation.
4. Prefix is exactly `incoming/`.
5. File was uploaded after trigger creation.
6. CloudTrail and CloudWatch logs.

## Scenario 2 — Recursive Invocations Cause High Cost

Root cause:

The trigger listens to the entire bucket, including `Finance/` and `Non-Finance/`.

Fix:

- Restrict trigger prefix to `incoming/`
- Add a code-level prefix check
- Set reserved concurrency temporarily to stop runaway executions

## Scenario 3 — Copy Succeeds but Original Is Not Deleted

Check:

- `s3:DeleteObject` permission
- Bucket policy explicit deny
- Object Lock retention
- Versioning behavior
- CloudWatch exception

## Scenario 4 — Files with Spaces Fail

S3 sends URL-encoded keys.

Use:

```python
unquote_plus(record["s3"]["object"]["key"])
```

## Scenario 5 — Duplicate Event Processes the Same File Twice

S3 is at-least-once.

Use:

- Deterministic destination key
- Source existence check
- Optional DynamoDB idempotency table for strict processing control

## Scenario 6 — Finance Files with `FIN_` Go to Non-Finance

Use case-insensitive matching:

```python
filename.lower().startswith("fin_")
```

## Scenario 7 — Thousands of Files Arrive Together

Check:

- Lambda concurrency
- Throttles
- Duration
- S3 request patterns
- Account concurrency quota

For controlled processing, send events through SQS and configure Lambda batch consumption.

## Scenario 8 — Business Wants a Third Category

Move rules into configuration:

```text
fin_ → Finance/
hr_  → Human-Resources/
ops_ → Operations/
default → Non-Finance/
```

Store rules in environment variables, DynamoDB or AppConfig.

## Scenario 9 — Security Team Rejects Broad IAM Permissions

Use prefix-level object ARNs and separate statements for read, write and delete.

## Scenario 10 — Audit Team Needs Proof of Every Move

Add structured CloudWatch logs containing:

- source key
- destination key
- event time
- request ID
- bucket
- ETag or version ID

Optionally write an audit record to DynamoDB.

## Scenario 11 — One Malformed Event Crashes the Batch

Handle every record independently, collect failures and raise only after processing all records.

## Scenario 12 — Destination Object Already Exists

Choose a business rule:

- Overwrite
- Skip
- Add timestamp
- Add UUID
- Preserve versions using S3 Versioning

## Scenario 13 — Lambda Duration Suddenly Increases

Check:

- API retries
- S3 latency
- Large object copy
- KMS encryption permissions
- Network dependencies
- CloudWatch logs and X-Ray

## Scenario 14 — Encrypted Bucket Uses a Customer KMS Key

Add KMS permissions for the Lambda role and update the KMS key policy.

## Scenario 15 — Files Must Be Routed to Separate Buckets

Use destination bucket environment variables and grant `PutObject` to both destination buckets. Keep the source trigger restricted to the upload bucket.
