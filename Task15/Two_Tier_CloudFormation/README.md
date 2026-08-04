# Project 15 — Two-Tier Web Architecture Using AWS CloudFormation

![Task 15 Architecture](infographic.png)

This project provisions a complete two-tier AWS web architecture using one CloudFormation template.

## Revised Architecture Requirement

An internet-facing Application Load Balancer must be associated with subnets in at least two Availability Zones. Therefore, the corrected implementation uses:

```text
Public Subnet A → ALB node, Bastion Host and NAT Gateway
Public Subnet B → Second ALB node
Private Subnet A → Private Web Server EC2
```

The ALB spans both public subnets, while the Web Server remains private and is reachable only from the ALB or the Bastion Host.

## Provisioned Resources

- VPC
- Two public subnets in separate Availability Zones
- One private web subnet
- Internet Gateway
- NAT Gateway and Elastic IP
- Public and private route tables
- ALB, Target Group and HTTP Listener
- Private Ubuntu EC2 web server
- Public Ubuntu Bastion Host
- Security Groups
- EC2 IAM role and instance profile
- User Data to install and configure NGINX
- Stack outputs for the ALB and instance addresses

## Documentation

1. [Part 1 — Architecture, Requirements and Prerequisites](documentation/README_PART1.md)
2. [Part 2 — CloudFormation Template Structure](documentation/README_PART2.md)
3. [Part 3 — Deploying and Validating the Stack](documentation/README_PART3.md)
4. [Part 4 — ALB, Bastion and Application Verification](documentation/README_PART4.md)
5. [Part 5 — Troubleshooting, Updates, Cleanup and Recommendations](documentation/README_PART5.md)

## Interview Preparation

- [Interview Guide](interview/Interview_Guide.md)
- [Production Scenarios](interview/Production_Scenarios.md)
- [AWS CLI Cheat Sheet](interview/AWS_CLI_CheatSheet.md)
- [Troubleshooting Guide](interview/Troubleshooting_Guide.md)

## Quick Deployment

```bash
aws cloudformation deploy \
  --template-file cloudformation/template.yaml \
  --stack-name task15-two-tier-web \
  --parameter-overrides \
    KeyName=<EC2_KEY_PAIR> \
    AdminCidr=<YOUR_PUBLIC_IP>/32 \
  --capabilities CAPABILITY_NAMED_IAM
```

After deployment:

```bash
aws cloudformation describe-stacks \
  --stack-name task15-two-tier-web \
  --query 'Stacks[0].Outputs'
```
