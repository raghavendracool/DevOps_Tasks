# Task 6 — Interview Guide

## 1. Explain the architecture.

An S3 ObjectCreated event invokes Lambda when a file is uploaded under `incoming/`. Lambda reads the filename, applies the prefix rule, copies the object to `Finance/` or `Non-Finance/`, deletes the original, and writes logs to CloudWatch.

## 2. Why use Lambda?

The workload is event-driven, short-lived and stateless. Lambda removes server management and scales automatically with upload volume.

## 3. Why use an S3 prefix filter?

It prevents recursive invocation when Lambda writes the classified object back to the same bucket.

## 4. Is the operation a true move?

S3 has no native rename or move API. The function performs copy followed by delete.

## 5. What happens if copy succeeds but delete fails?

Two copies remain. The function should log the failure, retry safely and use idempotent logic.

## 6. Are S3 events delivered exactly once?

No. They are generally delivered at least once, so duplicate events are possible.

## 7. How do you make the function idempotent?

Check whether the source object exists, use deterministic destination keys, and handle duplicate events safely.

## 8. How do you classify case-insensitively?

Use:

```python
filename.lower().startswith("fin_")
```

## 9. How do you handle spaces in object names?

Use `urllib.parse.unquote_plus` because S3 event object keys are URL encoded.

## 10. What IAM permissions are required?

`GetObject` on incoming objects, `PutObject` on destination prefixes and `DeleteObject` on incoming objects.

## 11. How would you classify by file content instead of filename?

Lambda could inspect metadata or file contents. For large files, use S3 Select, Step Functions, ECS, Glue or another asynchronous processing service.

## 12. How would you support multiple departments?

Use a configurable mapping, DynamoDB rules, object tags, metadata or EventBridge routing.

## 13. How would you monitor this?

CloudWatch Lambda metrics, logs, alarms on errors and throttles, S3 metrics, and optional failure destinations to SQS or SNS.

## 14. What happens under a large upload burst?

Lambda scales concurrently, but account concurrency, S3 request rates and downstream service limits must be considered.

## 15. How can you protect against accidental deletion?

Enable S3 Versioning and optionally Object Lock according to compliance requirements.

## 16. How would you test it?

Unit-test the classification function, use mocked boto3 calls, run Lambda test events, upload real files and verify destination objects and logs.

## 17. How would you deploy this in production?

Use Terraform, CloudFormation, AWS SAM or CDK with versioned Lambda releases, CI/CD, alarms and rollback.

## 18. Why keep the bucket private?

The classifier is backend automation. Public access is unnecessary and increases risk.

## 19. How would you handle files larger than Lambda limits?

S3 copy is server-side and does not download the object into Lambda memory. For content inspection, select a service appropriate to file size and processing duration.

## 20. How would you prevent overwriting an existing destination file?

Add a timestamp, UUID, version ID or checksum to the destination key, or check destination existence before copy.
