# 5. AWS Infrastructure Deployment

## Terraform

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
```

Update:

```text
admin_cidr
key_name
db_password
slack_webhook_secret_arn
```

Deploy:

```bash
terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
```

## Outputs

```bash
terraform output
```

Expected:

- ALB DNS name
- RDS endpoint
- S3 bucket
- Bastion public IP
- CloudWatch namespace

## CloudFormation

A smaller secondary stack is included under:

```text
infra/cloudformation/
```

It demonstrates the same IaC concepts using CloudFormation.

## Deployment Order

1. Network
2. IAM
3. S3
4. RDS
5. ALB and ASG
6. Lambda functions
7. EventBridge rules
8. Monitoring
9. Application deployment
