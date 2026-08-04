# Part 1 — Introduction, Architecture and Prerequisites

[← Main README](../README.md) | [Next: Part 2 →](README_PART2.md)

## Objective

Build a personal cloud-drive application where each logged-in user can:

- Upload files
- View files
- Download files
- Delete files
- Organize files under user-specific prefixes

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon EC2 | Hosts Flask, Gunicorn and NGINX |
| Amazon S3 | Stores uploaded files |
| AWS IAM | Grants EC2 secure S3 access |
| Amazon CloudWatch | Logs and monitoring |
| Route 53 | Optional domain |
| CloudFront | Optional secure global delivery |
| RDS MySQL | Optional production user metadata |

## Architecture

![Task 8 Architecture](../infographic.png)

## Storage Design

```text
s3://<BUCKET_NAME>/
└── users/
    ├── raghav/
    │   ├── documents/
    │   ├── images/
    │   └── videos/
    └── user2/
```

## Security Model

- S3 Block Public Access remains enabled.
- EC2 uses an IAM role.
- No AWS keys are stored in source code.
- Users can only access their own S3 prefix through application logic.
- Downloads use server-side streaming or presigned URLs.
- File names are sanitized before upload.

## Prerequisites

- AWS account
- Ubuntu EC2 key pair
- Python 3
- Git
- Basic Flask knowledge
- Unique S3 bucket name

## Recommended Region

```text
ap-south-1
```

## Naming Convention

| Resource | Name |
|---|---|
| EC2 | `task8-personal-cloud-drive` |
| S3 bucket | `raghav-task8-cloud-drive-<unique>` |
| IAM role | `task8-cloud-drive-ec2-role` |
| Security Group | `task8-cloud-drive-sg` |

## Checklist

- [ ] Region selected
- [ ] Bucket name prepared
- [ ] EC2 key pair available
- [ ] Private S3 design understood
- [ ] IAM role approach understood
