# Part 5 — Verification, Cleanup and Troubleshooting

[← Part 4](README_PART4.md) | [Main README](../README.md)

## End-to-End Verification

Upload:

```text
incoming/fin_invoice_001.csv
incoming/hr_policy.pdf
```

Expected:

```text
Finance/fin_invoice_001.csv
Non-Finance/hr_policy.pdf
```

Verify:

```bash
aws s3 ls s3://<BUCKET_NAME>/Finance/
aws s3 ls s3://<BUCKET_NAME>/Non-Finance/
aws s3 ls s3://<BUCKET_NAME>/incoming/
```

The `incoming/` prefix should be empty after successful processing.

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| Lambda not invoked | Trigger missing | S3 Event Notification |
| Recursive loop | Trigger on whole bucket | Prefix filter |
| Access denied | IAM policy incomplete | S3 object ARNs |
| Object not moved | Incorrect filename logic | CloudWatch logs |
| Object copied but not deleted | Missing `DeleteObject` | IAM permission |
| Spaces in filename fail | URL decoding missing | `unquote_plus` |
| Duplicate processing | At-least-once delivery | Idempotency |
| Timeout | Large object or retry | Lambda duration |

## Common Errors

### `AccessDenied`

Check the execution role policy:

```json
"s3:GetObject"
"s3:PutObject"
"s3:DeleteObject"
```

### Recursive Invocation

Remove the broad S3 trigger and configure:

```text
Prefix: incoming/
```

### File with Spaces Fails

S3 event keys are URL encoded. Use:

```python
from urllib.parse import unquote_plus
key = unquote_plus(record["s3"]["object"]["key"])
```

### Finance File Goes to Non-Finance

The comparison is case-sensitive by default.

Current rule:

```python
filename.startswith("fin_")
```

If required, make it case-insensitive:

```python
filename.lower().startswith("fin_")
```

## Cleanup

1. Delete S3 Event Notification.
2. Delete Lambda function.
3. Delete custom IAM policy.
4. Delete IAM execution role.
5. Delete CloudWatch Log Group if not required.
6. Empty the S3 bucket.
7. Delete the S3 bucket.

Commands:

```bash
aws s3 rm s3://<BUCKET_NAME>/ --recursive

aws s3api delete-bucket \
  --bucket <BUCKET_NAME> \
  --region ap-south-1
```

## Final Checklist

- [ ] Correct files classified
- [ ] No recursion
- [ ] CloudWatch logs available
- [ ] IAM follows least privilege
- [ ] Public access remains blocked
- [ ] Errors and throttles checked
- [ ] Resources cleaned up
