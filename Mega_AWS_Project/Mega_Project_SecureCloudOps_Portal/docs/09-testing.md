# 9. Testing and Verification

## Functional

- Register user
- Login
- Upload finance file
- Upload non-finance file
- List files
- Download file
- Delete file
- Confirm RDS metadata

## Infrastructure

- ALB healthy
- EC2 private
- RDS private
- Bastion restricted
- NAT egress
- ASG scale-out and scale-in

## Security

- S3 bucket private
- EBS encrypted
- IAM least privilege
- CloudTrail event captured
- SNS/Slack alert delivered

## Commands

```bash
./scripts/verify-deployment.sh
pytest backend/tests
cd frontend && npm test
```
