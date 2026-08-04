# 7. Security and Compliance Automation

## File Classification

Trigger:

```text
S3 ObjectCreated under uploads/
```

Rules:

```text
fin_* → classified/finance/
all others → classified/non-finance/
```

## Compliance Checks

- Required EC2 tags
- EBS encryption
- IAM access-key age
- Root MFA
- CloudTrail enabled
- AWS Config recorder
- Public SSH/RDP exposure
- S3 public access block

## Security Events

- CreateUser
- CreateAccessKey
- DeleteUser
- DeleteBucket
- StopLogging
- DeleteTrail
- Security Group ingress changes
- KMS key disable or deletion scheduling

## Notifications

- SNS email
- Optional Slack webhook
- CloudWatch logs
- Grafana alerts

## Secrets

Use AWS Secrets Manager for:

- Database password
- JWT secret
- Slack webhook
