# Part 2 — S3 Bucket, IAM Role and Security

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Create the S3 Bucket

Configure:

```text
Bucket name: raghav-task8-cloud-drive-<unique>
Region: ap-south-1
Block Public Access: Enabled
Versioning: Enabled
Default encryption: SSE-S3 or SSE-KMS
```

## Step 2 — Enable Versioning

```bash
aws s3api put-bucket-versioning \
  --bucket <BUCKET_NAME> \
  --versioning-configuration Status=Enabled
```

## Step 3 — Create the EC2 IAM Role

Create:

```text
Role name: task8-cloud-drive-ec2-role
Trusted service: EC2
```

Attach the supplied policy:

```text
iam/s3-access-policy.json
```

Replace `<BUCKET_NAME>`.

## Step 4 — Attach Role to EC2

```text
EC2 → Instance → Security → Modify IAM role
```

Choose:

```text
task8-cloud-drive-ec2-role
```

## Step 5 — S3 CORS

For this application, uploads pass through Flask, so S3 CORS is not required.

If you later upload directly from the browser using presigned URLs, configure restricted CORS for your domain.

## Step 6 — File Size Limits

The sample application uses:

```text
MAX_CONTENT_LENGTH = 50 MB
```

Adjust according to your requirement.

## Step 7 — Allowed File Types

The sample allows common documents, images, archives and videos.

For production:

- Scan uploads
- Validate MIME type
- Restrict executable files
- Consider Amazon GuardDuty Malware Protection for S3
- Use lifecycle policies

## Checklist

- [ ] Bucket created
- [ ] Public access blocked
- [ ] Encryption enabled
- [ ] Versioning enabled
- [ ] IAM role created
- [ ] Role attached to EC2
- [ ] Bucket name updated in application
