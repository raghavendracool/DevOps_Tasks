# 1. Project Scope and Learning Map

## Project Name

**SecureCloudOps Portal**

## Business Scenario

A company requires a secure internal document portal where employees upload operational, finance and general files. The application must be highly available, automatically classify uploaded documents, record metadata, and provide security and compliance monitoring.

## Skills Covered from Tasks 1–15

| Earlier Task | Mega Project Implementation |
|---|---|
| Multi-AZ EC2 | ALB and private EC2 Auto Scaling across AZs |
| Static website | React frontend build |
| AMI and EBS | Launch Template, encrypted gp3, AMI strategy |
| HA web app | ALB, Target Group, ASG and CPU scaling |
| Netflix/S3 media | S3-backed document delivery |
| Lambda file classifier | Finance/non-finance classification |
| Compliance Lambda | EC2 tags, EBS encryption, IAM key age |
| Cloud Drive | Upload, download, delete and user prefixes |
| IAM user security | CloudTrail/EventBridge security alerts |
| CloudTrail events | CreateAccessKey, DeleteUser, DeleteBucket |
| RDS application | MySQL users, metadata and login |
| SecOps metrics | CloudWatch custom metrics and Grafana |
| Bastion VPC | Bastion and private EC2 administration |
| Three-tier ALB/RDS | Complete production-like architecture |
| CloudFormation | Secondary IaC deployment example |

## Student Deliverables

- Running frontend and backend
- GitHub repository
- Architecture diagram
- Terraform deployment
- CloudFormation sample stack
- CI/CD pipeline
- Screenshots and test evidence
- Monitoring dashboard
- Security alert evidence
- Resume bullet points
- Interview explanation
