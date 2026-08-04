# Task 8 — Troubleshooting Guide

## Upload Failure

```text
Correct bucket environment variable?
        ↓
EC2 IAM role attached?
        ↓
PutObject allowed?
        ↓
KMS key permission?
        ↓
File size and extension allowed?
```

## NGINX 502

```bash
sudo systemctl status task8-cloud-drive
sudo journalctl -u task8-cloud-drive -n 100
sudo ss -lntp | grep 8000
```

## S3 AccessDenied

Check:

```text
IAM role policy
Bucket policy
Permission boundary
SCP
KMS key policy
```

## Production Recommendations

- Cognito authentication
- Presigned URLs
- RDS or DynamoDB
- ALB and Auto Scaling
- HTTPS
- WAF
- CloudTrail data events
- File scanning
- S3 versioning and lifecycle
