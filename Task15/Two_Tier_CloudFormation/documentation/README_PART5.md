# Part 5 — Troubleshooting, Updates, Cleanup and Recommendations

[← Part 4](README_PART4.md) | [Main README](../README.md)

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| Stack rollback | Resource creation failure | Stack events |
| ALB unavailable | Public routing or SG | IGW and port 80 |
| ALB uses only one subnet | Incorrect template or manual change | Select two public subnets in separate AZs |
| Target unhealthy | NGINX/User Data | cloud-init logs |
| Bastion SSH fails | Admin CIDR or key | Bastion SG |
| Web SSH fails | SG chaining | Bastion SG → Web SG |
| Web has no internet | NAT or private route | NAT state and route |
| IAM creation fails | Capability missing | Named IAM flag |
| Template invalid | YAML/property error | validate and cfn-lint |

## Cloud-Init Troubleshooting

On Web Server:

```bash
sudo tail -200 /var/log/cloud-init-output.log
sudo cloud-init status --long
sudo systemctl status nginx --no-pager
```

## Stack Update

Modify the template and run:

```bash
aws cloudformation deploy \
  --template-file cloudformation/template.yaml \
  --stack-name task15-two-tier-web \
  --parameter-overrides \
    KeyName=<EC2_KEY_PAIR> \
    AdminCidr=<YOUR_PUBLIC_IP>/32 \
  --capabilities CAPABILITY_NAMED_IAM
```

CloudFormation calculates and applies changes to the stack.

## Change Sets

For production review:

```bash
aws cloudformation create-change-set \
  --stack-name task15-two-tier-web \
  --change-set-name task15-review \
  --template-body file://cloudformation/template.yaml \
  --parameters \
    ParameterKey=KeyName,ParameterValue=<EC2_KEY_PAIR> \
    ParameterKey=AdminCidr,ParameterValue=<YOUR_PUBLIC_IP>/32 \
  --capabilities CAPABILITY_NAMED_IAM
```

Review before execution:

```bash
aws cloudformation describe-change-set \
  --stack-name task15-two-tier-web \
  --change-set-name task15-review
```

## Drift Detection

```bash
aws cloudformation detect-stack-drift \
  --stack-name task15-two-tier-web
```

Check result:

```bash
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id <DETECTION_ID>
```

## Production Recommendations

- Use a Launch Template and Auto Scaling Group.
- Place application instances in private subnets across at least two AZs.
- Use one NAT Gateway per AZ when availability requirements justify it.
- Use Systems Manager instead of a Bastion Host.
- Add HTTPS using ACM.
- Redirect HTTP to HTTPS.
- Add AWS WAF.
- Enable ALB access logs.
- Add CloudWatch alarms.
- Use VPC Flow Logs.
- Use S3 for templates and nested stacks.
- Use CloudFormation modules or nested stacks for reusable components.
- Run `cfn-lint`, security scans and policy checks in CI/CD.
- Use Change Sets before production updates.
- Enable termination protection for important stacks.
- Use StackSets for multi-account deployment.

## Cleanup

Delete the complete architecture as one stack:

```bash
./scripts/delete-stack.sh task15-two-tier-web
```

Or:

```bash
aws cloudformation delete-stack \
  --stack-name task15-two-tier-web

aws cloudformation wait stack-delete-complete \
  --stack-name task15-two-tier-web
```

## Deletion Order

CloudFormation automatically resolves dependencies and deletes:

1. Listener and ALB
2. Target Group
3. EC2 instances
4. NAT Gateway and EIP
5. Routes and route tables
6. Security Groups
7. Subnets
8. Internet Gateway
9. IAM instance profile and role
10. VPC

## Final Checklist

- [ ] ALB verified
- [ ] Target healthy
- [ ] Bastion path verified
- [ ] Web Server private
- [ ] Template stored in GitHub
- [ ] Stack deleted after lab
- [ ] NAT Gateway and EIP removed
