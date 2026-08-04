# SecureCloudOps Portal — AWS DevOps Mega Project

![High-Level Architecture](architecture.png)

## Project Summary

SecureCloudOps Portal combines the skills practiced across all 15 AWS projects into one end-to-end, resume-ready application.

Students build and deploy:

- A real React frontend
- A FastAPI backend
- Amazon RDS MySQL for users and file metadata
- Amazon S3 for private document storage
- AWS Lambda for automatic file classification
- CloudTrail and EventBridge security monitoring
- Scheduled compliance checks
- Custom CloudWatch metrics
- Grafana dashboards and alerts
- A highly available VPC with ALB, Auto Scaling, private EC2 and private RDS
- Bastion Host and Systems Manager administration
- Terraform and CloudFormation Infrastructure as Code
- GitHub Actions CI/CD

## Application Use Case

Users register and log in to a personal cloud-drive portal. They can upload, list, download and delete documents.

Uploaded files are stored in a private S3 bucket:

```text
uploads/<user-id>/<filename>
```

Files beginning with `fin_` are classified automatically:

```text
fin_invoice.pdf → classified/finance/<user-id>/fin_invoice.pdf
notes.txt       → classified/non-finance/<user-id>/notes.txt
```

The application records file metadata in Amazon RDS MySQL.

Security and compliance automations detect:

- Missing EC2 tags
- Unencrypted EBS volumes
- Old IAM access keys
- IAM user creation
- IAM access-key creation
- IAM user deletion
- S3 bucket deletion
- Selected high-risk CloudTrail events

## Architecture Tiers

```text
Users
  ↓
Route 53 / ALB
  ↓
Private EC2 Auto Scaling Group
  ├── NGINX
  ├── React frontend
  └── FastAPI backend
        ├── Amazon RDS MySQL
        └── Amazon S3
```

Automation:

```text
S3 Upload → EventBridge/S3 Event → File Classification Lambda
CloudTrail → EventBridge → Security Monitoring Lambda → SNS/Slack
Schedule → Compliance Lambda → CloudWatch Metrics → Grafana
```

## Repository Structure

```text
Mega_Project_SecureCloudOps_Portal/
├── README.md
├── architecture.png
├── docs/
├── frontend/
├── backend/
├── infra/
│   ├── terraform/
│   └── cloudformation/
├── lambdas/
├── monitoring/
├── scripts/
├── interview/
├── resume/
└── .github/workflows/
```

## Documentation Order

1. [Project Scope and Learning Map](docs/01-project-scope.md)
2. [Tools and Software](docs/02-tools-and-software.md)
3. [Architecture and Networking](docs/03-architecture.md)
4. [Local Development](docs/04-local-development.md)
5. [AWS Infrastructure Deployment](docs/05-aws-deployment.md)
6. [Application Deployment](docs/06-application-deployment.md)
7. [Security and Compliance Automation](docs/07-security-compliance.md)
8. [Monitoring and Grafana](docs/08-monitoring.md)
9. [Testing and Verification](docs/09-testing.md)
10. [Troubleshooting and Cleanup](docs/10-troubleshooting-cleanup.md)
11. [Resume and Interview Guide](resume/Resume_Talking_Points.md)

## Quick Start

### Local

```bash
docker compose up --build
```

Open:

```text
Frontend: http://localhost:3000
Backend API: http://localhost:8000/docs
```

### AWS Infrastructure

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

### Production Validation

```bash
./scripts/verify-deployment.sh
```

## Important

This is a training and portfolio project. Before production use:

- Replace sample secrets
- Use AWS Secrets Manager
- Enable HTTPS
- Enable WAF
- Use Multi-AZ RDS
- Configure backups and retention
- Complete security review
- Perform load and recovery testing
