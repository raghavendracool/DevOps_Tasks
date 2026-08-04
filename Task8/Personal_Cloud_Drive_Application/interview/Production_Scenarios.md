# Task 8 — Real-Time Production Scenarios

## Scenario 1 — Upload Returns AccessDenied

Check:

- EC2 IAM role attached
- Bucket ARN in policy
- S3 Block Public Access does not block IAM access
- KMS key permissions
- Application environment bucket name

## Scenario 2 — User Can Access Another User's File

This is a critical authorization issue.

Fix:

- Never trust a username from the URL
- Build the S3 prefix from the authenticated session
- Add authorization tests
- Use presigned URLs only after ownership validation

## Scenario 3 — Large Files Fail

Check:

- Flask `MAX_CONTENT_LENGTH`
- NGINX `client_max_body_size`
- Gunicorn timeout
- EC2 memory
- Use multipart or presigned upload

## Scenario 4 — EC2 Fails

Files remain safe in S3, but the application becomes unavailable.

Use ALB and Auto Scaling for high availability.

## Scenario 5 — Users Accidentally Delete Files

Enable S3 Versioning and add a restore workflow.

## Scenario 6 — Download Is Slow

Use presigned S3 URLs and CloudFront instead of proxying file bytes through EC2.

## Scenario 7 — Two Files Have the Same Name

Choose a rule:

- Overwrite
- Add timestamp
- Add UUID
- Preserve versions

## Scenario 8 — Virus Is Uploaded

Quarantine new uploads and scan them before making them downloadable.

## Scenario 9 — Session Is Lost After Scaling Out

Use server-side shared sessions in Redis, DynamoDB or another shared store.

## Scenario 10 — Database Is Locked

SQLite does not scale well for concurrent production traffic. Move users and metadata to RDS or DynamoDB.

## Scenario 11 — User Storage Quotas Are Required

Calculate prefix size and enforce per-user limits before upload.

## Scenario 12 — Compliance Requires Audit History

Enable CloudTrail data events, application audit records and immutable retention.

## Scenario 13 — S3 Costs Increase

Review object sizes, requests, data transfer, lifecycle classes and abandoned versions.

## Scenario 14 — A Bucket Becomes Public

Use Block Public Access, AWS Config, Security Hub and preventive SCPs.

## Scenario 15 — File Names Contain Special Characters

Use secure filename handling and UTF-8-safe object-key rules.

## Scenario 16 — HTTPS Is Required

Use ALB with ACM or NGINX with Let's Encrypt.

## Scenario 17 — App Must Support Thousands of Users

Use Cognito, ALB, ASG, RDS/DynamoDB, presigned transfers and CloudFront.

## Scenario 18 — User Wants File Sharing

Create explicit share records and time-limited presigned URLs.

## Scenario 19 — User Wants Folder Rename

S3 has no true folder rename; copy all objects to the new prefix and delete old keys.

## Scenario 20 — Ransomware Deletes Many Files

Use versioning, MFA Delete where appropriate, Object Lock and anomaly monitoring.
