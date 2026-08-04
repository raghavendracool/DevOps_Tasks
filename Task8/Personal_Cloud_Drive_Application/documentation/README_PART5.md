# Part 5 — Testing, Cleanup and Troubleshooting

[← Part 4](README_PART4.md) | [Main README](../README.md)

## End-to-End Testing

1. Register user `raghav`.
2. Log in.
3. Upload a PDF.
4. Upload an image.
5. Confirm S3 keys:

```text
users/raghav/<filename>
```

6. Download the file.
7. Delete the file.
8. Confirm it no longer appears.

## Useful Commands

```bash
sudo systemctl status task8-cloud-drive --no-pager
sudo journalctl -u task8-cloud-drive -n 100 --no-pager
sudo systemctl status nginx --no-pager
sudo tail -100 /var/log/nginx/error.log
aws s3 ls s3://<BUCKET_NAME>/users/ --recursive
```

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| Upload fails | IAM role or bucket name | EC2 role and environment |
| Download denied | Wrong user prefix | Session and S3 key |
| NGINX 502 | Gunicorn down | systemd logs |
| Login fails | SQLite issue | database file permissions |
| Large file fails | size limit | `MAX_CONTENT_LENGTH` |
| S3 AccessDenied | policy mismatch | bucket ARN |
| Files exposed | public bucket | Block Public Access |

## Cleanup

1. Stop and terminate EC2.
2. Release Elastic IP.
3. Delete Route 53 records.
4. Empty S3 bucket.
5. Delete all object versions.
6. Delete S3 bucket.
7. Delete IAM role and policy.
8. Delete CloudWatch log groups if not needed.

## Production Improvements

- Amazon Cognito authentication
- Private subnets and ALB
- RDS or DynamoDB
- Presigned uploads and downloads
- CloudFront
- WAF
- GuardDuty Malware Protection for S3
- S3 lifecycle rules
- Object version restore
- MFA for sensitive actions
- Audit trail in CloudTrail
