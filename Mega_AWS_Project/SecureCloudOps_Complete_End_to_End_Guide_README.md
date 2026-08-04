# SecureCloudOps Portal

## Complete End-to-End Implementation Guide

![SecureCloudOps Portal Architecture](Mega_Project_SecureCloudOps_Portal/architecture.png)

> This Markdown guide is designed to be placed in the repository root, next to the `Mega_Project_SecureCloudOps_Portal` folder.

---

# 1. What Is This Project About?

SecureCloudOps Portal is a real three-tier cloud-drive and SecOps application that combines the hands-on learning from all 15 AWS tasks into one portfolio project. It gives students one business problem to design, build, automate, secure, monitor and explain in an interview.

## Business Use Case

A company needs a secure internal portal where users register, log in and manage files. Finance files must be automatically classified, file metadata must be stored in MySQL, the application must remain highly available, and the AWS environment must continuously detect security and compliance violations.

## What the User Can Do

- Register and log in using the React frontend and FastAPI backend.
- Upload documents to a private Amazon S3 bucket.
- View uploaded files and their classification status.
- Download files through short-lived S3 presigned URLs.
- Delete files from both S3 and the metadata database.
- Use a highly available application endpoint exposed through an ALB.

## What AWS Automation Does

- Classifies files beginning with fin\_ into the Finance prefix.
- Routes other files into the Non-Finance prefix.
- Checks EC2 tags, EBS encryption and IAM access-key age.
- Detects CloudTrail events such as IAM user creation, access-key creation, IAM user deletion and S3 bucket deletion.
- Publishes CloudWatch custom metrics and sends SNS or Slack notifications.
- Displays infrastructure, security and compliance metrics in Grafana.

## Resume-Level Project Description

> **Project statement:** Designed and deployed a highly available AWS three-tier application using VPC, ALB, Auto Scaling, private EC2, Amazon RDS MySQL and private Amazon S3. Developed a React frontend and FastAPI backend with authentication and file operations. Implemented Lambda-based file classification, CloudTrail/EventBridge security monitoring, scheduled compliance checks, CloudWatch metrics, Grafana dashboards, Terraform Infrastructure as Code and GitHub Actions CI.

# 2. Architecture Explained to the Team

| **Tier / Area**  | **Components**                                          | **Purpose**                                                          |
|------------------|---------------------------------------------------------|----------------------------------------------------------------------|
| Entry tier       | Route 53, optional CloudFront/WAF, ALB                  | Receives user traffic and exposes only the approved public endpoint. |
| Application tier | NGINX, React, FastAPI on private EC2 Auto Scaling Group | Runs the frontend and backend without public EC2 addresses.          |
| Data tier        | Amazon RDS MySQL in private DB subnets                  | Stores users and file metadata.                                      |
| Object storage   | Private and encrypted S3 bucket                         | Stores uploaded files and classified files.                          |
| Automation       | Lambda and EventBridge                                  | Classifies files and runs security/compliance checks.                |
| Observability    | CloudWatch, SNS and Grafana                             | Logs, metrics, dashboards and alerts.                                |
| Administration   | Systems Manager or restricted Bastion Host              | Provides controlled access to private EC2 instances.                 |

## Traffic Flow

> User Browser  
> ↓  
> Application Load Balancer in two public subnets  
> ↓  
> NGINX + React + FastAPI on private EC2 instances  
> ↓  
> Amazon RDS MySQL and private Amazon S3

## Automation Flow

> S3 uploads/ prefix → S3 Event → File Classification Lambda  
> CloudTrail API event → EventBridge → Security Lambda → SNS/Slack  
> EventBridge schedule → Compliance Lambda → CloudWatch Metrics → Grafana

## Security Group Flow

> Internet → ALB SG :80/:443  
> ALB SG → Application SG :80  
> Bastion SG → Application SG :22  
> Application SG → RDS SG :3306

> **Public versus private:** The ALB is public. Application EC2 and RDS remain private. A Bastion Host is optional and must be restricted to the trainer or company public CIDR. Systems Manager is the preferred modern administration method.

# 3. What Is Automatic and What Is Not?

| **Action**                              | **What It Does**                                                | **Creates AWS Resources?**                     |
|-----------------------------------------|-----------------------------------------------------------------|------------------------------------------------|
| git clone                               | Downloads repository files to the laptop.                       | No                                             |
| docker compose up --build               | Builds frontend, backend and MySQL containers locally.          | No                                             |
| terraform init                          | Downloads Terraform providers and initializes the folder.       | No                                             |
| terraform plan                          | Shows proposed AWS changes.                                     | No                                             |
| terraform apply                         | Creates the resources defined in Terraform.                     | Yes                                            |
| Running Lambda Python locally           | Executes code only if manually tested with mocked/local events. | No                                             |
| Terraform Lambda resources and triggers | Packages, creates and connects Lambda to S3/EventBridge.        | Yes, only after added and applied              |
| Importing Grafana JSON                  | Creates dashboard panels in an existing Grafana workspace.      | No AWS workspace unless separately provisioned |

> **Current repository status:** The repository contains working application code and Lambda source files. The core Terraform creates VPC, subnets, NAT, ALB, ASG, RDS, S3, Bastion, IAM and SNS. The initial version does not fully package and deploy all three Lambda functions, S3 notifications, EventBridge rules, CloudTrail, AWS Config, Grafana workspace, Slack secret or every CloudWatch alarm. These must be added before claiming one-command deployment.

## Definition of “Everything Works”

- Local frontend and backend pass testing.
- Terraform creates all core AWS resources.
- Database schema is initialized.
- Application code is deployed to private EC2 instances.
- S3 event invokes the file-classification Lambda.
- Scheduled compliance Lambda publishes metrics.
- CloudTrail EventBridge rule invokes security Lambda.
- SNS/Slack test notification succeeds.
- Grafana dashboard displays real metrics.
- ALB health and application workflows pass.
- terraform destroy removes chargeable resources.

# 4. Team Roles and Ownership

| **Role**              | **Main Responsibility**                                   | **Evidence to Present**                        |
|-----------------------|-----------------------------------------------------------|------------------------------------------------|
| Team Lead / Architect | Explain architecture, dependencies and deployment order.  | Architecture walkthrough and final demo.       |
| Frontend Engineer     | React login, dashboard and file actions.                  | Working UI and frontend build.                 |
| Backend Engineer      | FastAPI authentication, RDS models and S3 APIs.           | Swagger tests and database records.            |
| Cloud Engineer        | VPC, ALB, ASG, RDS, S3 and Security Groups.               | Terraform plan/apply and AWS console evidence. |
| Automation Engineer   | Lambda packaging, S3 trigger and EventBridge rules.       | Lambda logs and classified objects.            |
| SecOps Engineer       | CloudTrail, compliance checks, metrics and notifications. | SNS/Slack alerts and CloudWatch logs.          |
| Monitoring Engineer   | Grafana dashboard and alarms.                             | Dashboard and alert test.                      |
| QA / Release Engineer | Test plan, CI and cleanup validation.                     | Test report and GitHub Actions result.         |

# 5. Software and Accounts Required

| **Tool / Account** | **Recommended Version** | **How It Is Used**                    |
|--------------------|-------------------------|---------------------------------------|
| AWS account        | Training/sandbox        | Creates all cloud resources.          |
| Git                | Current stable          | Clone, branch, commit and push.       |
| GitHub             | Repository access       | Source control and GitHub Actions.    |
| VS Code            | Current stable          | Code editing and terminal.            |
| Python             | 3.12+                   | FastAPI and Lambda.                   |
| Node.js            | 20+                     | React/Vite frontend.                  |
| Docker Desktop     | Current stable          | Local frontend/backend/MySQL testing. |
| AWS CLI            | v2                      | Credential and resource validation.   |
| Terraform          | 1.6+                    | Primary IaC deployment.               |
| MySQL Workbench    | Current stable          | RDS schema and query verification.    |
| Postman or curl    | Current stable          | API testing.                          |
| SSH client         | OpenSSH                 | Bastion/ProxyJump troubleshooting.    |

## Verify Tools

> git --version  
> python --version  
> node --version  
> npm --version  
> docker --version  
> aws --version  
> terraform version

# 6. Every Key, Secret and Variable You Need

| **Name**              | **Where Used**                                    | **Example / Source**                             | **Sensitive?** |
|-----------------------|---------------------------------------------------|--------------------------------------------------|----------------|
| AWS_ACCESS_KEY_ID     | AWS CLI/Terraform when using IAM user credentials | Configured by aws configure                      | Yes            |
| AWS_SECRET_ACCESS_KEY | AWS CLI/Terraform                                 | Configured by aws configure                      | Yes            |
| AWS_SESSION_TOKEN     | Temporary/SSO credentials                         | Provided by AWS session                          | Yes            |
| AWS_REGION            | AWS CLI, backend and Terraform                    | ap-south-1                                       | No             |
| admin_cidr            | Bastion Security Group                            | YourPublicIP/32                                  | No             |
| key_name              | EC2 Launch Template and Bastion                   | Existing EC2 key-pair name                       | No             |
| PEM key file          | SSH connection                                    | Downloaded when key pair is created              | Yes            |
| db_username           | RDS and backend                                   | appuser                                          | No             |
| db_password           | RDS and backend                                   | Strong unique password                           | Yes            |
| DATABASE_URL          | Backend                                           | mysql+pymysql://...                              | Yes            |
| JWT_SECRET            | Backend token signing                             | Long random value                                | Yes            |
| S3_BUCKET_NAME        | Backend and Lambda                                | Terraform output                                 | No             |
| SNS_TOPIC_ARN         | Lambda notifications                              | Terraform output                                 | No             |
| Slack webhook         | Security alerts                                   | Slack Incoming Webhook stored in Secrets Manager | Yes            |
| GitHub repository URL | EC2 User Data deployment                          | Repository clone URL                             | No             |
| GitHub PAT            | Only for private repository clone                 | GitHub secret or deployment key                  | Yes            |

## Generate a JWT Secret

> python -c "import secrets; print(secrets.token_urlsafe(48))"

## AWS CLI Authentication

> aws configure  
> aws sts get-caller-identity  
> aws configure get region

> **Preferred authentication:** Use AWS IAM Identity Center / SSO or short-lived credentials when available. Do not commit AWS keys, database passwords, JWT secrets, PEM files or Slack webhooks to GitHub.

# 7. Phase 1 — Clone and Test Everything Locally

## Step 1: Clone

> git clone https://github.com/\<USERNAME\>/\<REPOSITORY\>.git  
> cd \<REPOSITORY\>

## Step 2: Create Local Environment

> cp .env.example .env

For local Docker testing, use the following values:

> DATABASE_URL=mysql+pymysql://appuser:app-password@db:3306/securecloudops  
> AWS_REGION=ap-south-1  
> S3_BUCKET_NAME=securecloudops-local  
> JWT_SECRET=\<GENERATED_SECRET\>  
> ACCESS_TOKEN_EXPIRE_MINUTES=60

> **Local S3 limitation:** The current backend uses boto3. A normal local Docker environment does not provide a real S3 bucket. For a complete local-only test, either configure LocalStack/MinIO and endpoint support in the backend, or use an AWS sandbox bucket with credentials. Authentication and database health can still be tested locally without completing S3 operations.

## Step 3: Build Containers

> docker compose config  
> docker compose up --build -d  
> docker compose ps  
> docker compose logs -f backend

## Step 4: Verify

> curl http://localhost:8000/health  
> curl http://localhost:8000/api/health/db  
> curl -I http://localhost:3000

## Step 5: UI Test

1.  Open http://localhost:3000.

2.  Register a test user.

3.  Log in.

4.  Confirm the dashboard opens.

5.  Open http://localhost:8000/docs and test the API.

## Step 6: Stop Local Environment

> docker compose down  
> docker compose down -v \# also removes local MySQL data

# 8. Phase 2 — Prepare AWS Deployment Values

## Find Your Public IP

> curl -s https://checkip.amazonaws.com

Append /32, for example: 203.0.113.10/32.

## Confirm EC2 Key Pair

> aws ec2 describe-key-pairs --query 'KeyPairs\[\].KeyName' --output table

## Create terraform.tfvars

> cd infra/terraform  
> cp terraform.tfvars.example terraform.tfvars
>
> aws_region = "ap-south-1"  
> admin_cidr = "\<YOUR_PUBLIC_IP\>/32"  
> key_name = "\<EXISTING_KEY_PAIR_NAME\>"  
> db_password = "\<STRONG_DATABASE_PASSWORD\>"  
> instance_type = "t3.small"  
> desired_capacity = 2  
> min_size = 2  
> max_size = 4

> **Do not commit:** terraform.tfvars, .env, PEM files and Terraform state are excluded through .gitignore. Verify this before pushing.

# 9. Phase 3 — Deploy Core AWS Infrastructure

## Terraform Validation

> terraform init  
> terraform fmt -recursive  
> terraform fmt -check -recursive  
> terraform validate  
> terraform plan -out=tfplan

## Review the Plan

- Confirm the expected AWS account and Region.
- Confirm VPC CIDR and subnet CIDRs.
- Confirm two public, two application-private and two DB-private subnets.
- Confirm only ALB and Bastion receive public access.
- Confirm EBS, RDS and S3 encryption.
- Confirm NAT Gateway, ALB and RDS costs are acceptable.

## Apply

> terraform apply tfplan

## Capture Outputs

> terraform output  
> terraform output -raw alb_dns_name  
> terraform output -raw s3_bucket_name  
> terraform output -raw bastion_public_ip

## What Core Terraform Creates

- VPC, public subnets, application-private subnets and DB-private subnets.
- Internet Gateway, NAT Gateway, route tables and associations.
- ALB, Target Group, Listener, Launch Template and Auto Scaling Group.
- Private RDS MySQL and DB subnet group.
- Private encrypted and versioned S3 bucket.
- Security Groups, EC2 role, SSM access and S3 permissions.
- Bastion Host and SNS topic.

# 10. Phase 4 — Initialize the Database

The FastAPI application creates ORM tables when it starts, but the database itself and application credentials must exist. Terraform creates the database name and user from the RDS master configuration in this training design.

## Get RDS Endpoint

> terraform output -raw rds_endpoint

## Connect Through Bastion

> ssh -i \<KEY\>.pem ubuntu@\<BASTION_PUBLIC_IP\>

## From a Private Application Instance

> mysql -h \<RDS_ENDPOINT\> -u appuser -p securecloudops  
> SHOW TABLES;  
> SELECT COUNT(\*) FROM users;

> **Recommended production change:** Store the RDS credentials in AWS Secrets Manager and grant EC2 only secretsmanager:GetSecretValue for that exact secret. Do not write the database password directly into EC2 User Data or Terraform state for production.

# 11. Phase 5 — Deploy the Application to EC2

## Mandatory Repository Placeholder

Update this file before terraform apply:

> infra/terraform/user_data.sh.tftpl

Replace:

> https://github.com/\<YOUR_GITHUB_USERNAME\>/\<YOUR_REPOSITORY\>.git

## Public Repository

The EC2 User Data can clone it directly.

## Private Repository

- Use a GitHub deploy key, GitHub App token or CodeDeploy artifact.
- Store the credential in Secrets Manager or SSM Parameter Store.
- Do not place a PAT directly in User Data.

## Validate User Data on an EC2 Instance

> sudo cloud-init status --long  
> sudo tail -200 /var/log/cloud-init-output.log  
> sudo docker ps  
> sudo docker compose -f /opt/securecloudops/app/docker-compose.yml ps  
> curl http://localhost/health

> **Current deployment gap:** The provided docker-compose.yml starts a local MySQL container. On AWS, the application should start only frontend and backend and use RDS. Before the final AWS deployment, create a production compose file without the db service, or use service profiles. This correction is required for a clean production-like deployment.

# 12. Phase 6 — Deploy and Connect Lambda Functions

To make the project complete, Terraform must package and deploy all Lambda functions and connect their triggers.

## Lambda 1: File Classifier

| **Setting** | **Value**                                         |
|-------------|---------------------------------------------------|
| Source      | lambdas/file_classifier/lambda_function.py        |
| Runtime     | Python 3.12                                       |
| Trigger     | S3 ObjectCreated                                  |
| Prefix      | uploads/                                          |
| Destination | classified/finance/ or classified/non-finance/    |
| Permissions | S3 read/write/delete and CloudWatch PutMetricData |

## Lambda 2: Compliance Monitor

| **Setting**    | **Value**                                                   |
|----------------|-------------------------------------------------------------|
| Source         | lambdas/compliance_monitor/lambda_function.py               |
| Trigger        | EventBridge schedule                                        |
| Suggested rate | Every 6 hours; 15 minutes for demo                          |
| Environment    | SNS_TOPIC_ARN, REQUIRED_TAGS, MAX_ACCESS_KEY_AGE_DAYS       |
| Permissions    | Describe EC2/EBS, list IAM keys, PutMetricData, SNS publish |

## Lambda 3: Security Monitor

| **Setting** | **Value**                                                                       |
|-------------|---------------------------------------------------------------------------------|
| Source      | lambdas/security_monitor/lambda_function.py                                     |
| Trigger     | EventBridge CloudTrail event patterns                                           |
| Events      | CreateUser, CreateAccessKey, DeleteUser, DeleteBucket, StopLogging, DeleteTrail |
| Environment | SNS_TOPIC_ARN                                                                   |
| Permissions | PutMetricData and SNS publish                                                   |

## Packaging Example

> cd lambdas/file_classifier  
> zip -j /tmp/file_classifier.zip lambda_function.py  
> aws lambda update-function-code --function-name securecloudops-file-classifier --zip-file fileb:///tmp/file_classifier.zip

> **Full automation requirement:** Add archive_file data sources, aws_lambda_function resources, aws_lambda_permission resources, aws_s3_bucket_notification, aws_cloudwatch_event_rule and aws_cloudwatch_event_target resources to Terraform. Without these, Lambda code remains only source code in the repository.

# 13. Phase 7 — CloudTrail, EventBridge, SNS and Slack

## CloudTrail

- Create or verify a multi-region trail.
- Enable management events.
- Enable log-file validation.
- Store logs in an encrypted S3 bucket with retention.

## EventBridge Patterns

> {  
> "source": \["aws.iam", "aws.s3", "aws.cloudtrail"\],  
> "detail-type": \["AWS API Call via CloudTrail"\],  
> "detail": {  
> "eventName": \["CreateUser", "CreateAccessKey", "DeleteUser", "DeleteBucket", "StopLogging", "DeleteTrail"\]  
> }  
> }

## SNS Email Subscription

> aws sns subscribe --topic-arn \<SNS_TOPIC_ARN\> --protocol email --notification-endpoint \<TEAM_EMAIL\>

The recipient must confirm the subscription email.

## Slack Webhook

6.  Create a Slack Incoming Webhook for the security channel.

7.  Store it in Secrets Manager; do not store it in code.

8.  Grant only the security Lambda permission to retrieve the secret.

9.  Send a controlled test and verify Slack HTTP success in CloudWatch Logs.

# 14. Phase 8 — Monitoring and Grafana

## CloudWatch Namespace

> SecureCloudOps

## Custom Metrics

- ComplianceScore
- NonCompliantResources
- SecurityEvents
- FileClassificationSuccess
- FileClassificationFailure
- ApplicationErrors
- UploadCount

## AWS Service Metrics

- ALB RequestCount, TargetResponseTime, HTTPCode_Target_5XX_Count and UnHealthyHostCount.
- ASG InServiceInstances and GroupDesiredCapacity.
- EC2 CPUUtilization.
- RDS CPUUtilization and DatabaseConnections.
- Lambda Errors, Duration and Throttles.

## Grafana Setup

10. Create an Amazon Managed Grafana workspace or use a lab Grafana server.

11. Configure CloudWatch as the data source.

12. Grant CloudWatch read permissions to the Grafana workspace role.

13. Import monitoring/grafana/dashboard.json.

14. Create contact points for email or Slack.

15. Create alert rules and run a test notification.

## Recommended Alerts

| **Alert**               | **Condition**                 |
|-------------------------|-------------------------------|
| Application unavailable | UnHealthyHostCount \>= 1      |
| ALB errors              | Target 5XX \>= 5 in 5 minutes |
| High CPU                | EC2 or RDS CPU \> 80%         |
| Lambda failure          | Errors \>= 1                  |
| Compliance failure      | ComplianceScore \< 100        |
| Security event          | SecurityEvents \>= 1          |

# 15. End-to-End Verification Demo

16. Open the ALB DNS name.

17. Register and log in.

18. Upload fin_invoice.txt.

19. Upload project_notes.txt.

20. Verify S3 uploads/ objects trigger Lambda.

21. Verify files appear under classified/finance and classified/non-finance.

22. Verify file metadata in RDS.

23. Download a file using the presigned URL.

24. Delete a file.

25. Refresh /api/instance repeatedly and show multiple EC2 instances.

26. Generate CPU load and show ASG scale-out.

27. Trigger a controlled security event in a sandbox.

28. Verify SNS or Slack alert.

29. Run compliance Lambda and verify CloudWatch metrics.

30. Open Grafana and show dashboard panels and alert status.

## Verification Commands

> curl http://\<ALB_DNS\>/health  
> curl http://\<ALB_DNS\>/api/health/db  
> aws s3 ls s3://\<BUCKET\>/ --recursive  
> aws logs tail /aws/lambda/securecloudops-file-classifier --follow  
> aws cloudwatch list-metrics --namespace SecureCloudOps  
> aws autoscaling describe-scaling-activities --auto-scaling-group-name \<ASG_NAME\>

# 16. Common Problems and Fixes

| **Problem**                  | **Likely Cause**                                | **Fix**                                               |
|------------------------------|-------------------------------------------------|-------------------------------------------------------|
| Frontend loads but API fails | Incorrect NGINX proxy or backend container down | Check frontend nginx.conf, docker logs and port 8000. |
| Database health fails        | RDS SG, endpoint or password                    | Verify App SG → RDS SG 3306 and DATABASE_URL.         |
| EC2 User Data fails          | Repository placeholder, NAT or Docker install   | Review cloud-init-output.log and private route.       |
| ALB returns 503              | Targets unhealthy                               | Check /health, App SG and container status.           |
| Upload gets AccessDenied     | EC2 S3 role policy or wrong bucket              | Check instance role and S3 ARN.                       |
| Classifier does not run      | S3 notification or Lambda permission missing    | Add S3 trigger and aws_lambda_permission.             |
| Security alert missing       | CloudTrail/EventBridge/SNS incomplete           | Verify event history, rule, target and subscription.  |
| Grafana has no data          | Wrong Region/namespace/role                     | Select correct CloudWatch Region and permissions.     |
| Terraform destroy fails      | Non-empty/versioned S3 or manual dependency     | Empty all versions and remove external dependencies.  |

# 17. Cost Control and Cleanup

The most expensive lab resources are generally NAT Gateway, ALB and RDS. Students must destroy the project after evidence is collected.

## Before Destroy

- Download screenshots and logs.
- Export Grafana dashboard JSON.
- Take a final RDS snapshot only if required.
- Delete or archive important S3 test files.

## Destroy

> cd infra/terraform  
> terraform plan -destroy  
> terraform destroy

## Verify No Charges Remain

- No NAT Gateway.
- No Elastic IP.
- No ALB or Target Group.
- No EC2 or Auto Scaling Group.
- No RDS instance or unwanted snapshot.
- No non-empty S3 bucket.
- No Lambda, EventBridge rules or Grafana workspace.
- No unused Secrets Manager secret with ongoing rotation.

> **Never assume cleanup succeeded:** Review the AWS console and Cost Explorer/Billing after the lab. Terraform destroys only resources it manages in its state. Manually created resources must be deleted separately.

# 18. Work Required for True One-Command Deployment

The following enhancements are required before the team can accurately say that terraform apply creates the entire project:

- Create production Docker Compose or ECS deployment without a local MySQL container.
- Move database and JWT secrets to Secrets Manager.
- Add Lambda ZIP packaging and aws_lambda_function resources.
- Add S3 event notification and Lambda invoke permission.
- Add EventBridge schedule and CloudTrail security event rules.
- Provision CloudTrail and AWS Config.
- Provision SNS subscriptions or document confirmation step.
- Provision CloudWatch alarms.
- Provision Amazon Managed Grafana workspace and role, or document manual import.
- Add Route 53, ACM HTTPS and optional WAF.
- Add database migration job.
- Add CI/CD deployment workflow using OIDC rather than long-lived AWS keys.
- Add automated integration tests and rollback.

> **Recommended classroom approach:** Run the project in phases. First validate locally, then deploy core infrastructure, then assign Lambda/SecOps/monitoring modules to student groups, and finally integrate them for the end-to-end demonstration.

# 19. Trainer Presentation Flow

31. Explain the business problem and user journey.

32. Explain the six-subnet VPC and Security Group chaining.

33. Show the repository structure.

34. Explain local Docker testing and its limitations.

35. Show terraform plan and the resources it creates.

36. Show ALB, ASG, private EC2 and private RDS.

37. Demonstrate user login and file operations.

38. Demonstrate S3 classification Lambda.

39. Demonstrate CloudTrail security alert.

40. Demonstrate compliance metrics and Grafana.

41. Show GitHub Actions validation.

42. Explain cost, recovery and production improvements.

43. Finish with resume bullets and interview questions.

# 20. Final Go-Live Checklist

| **Area**      | **Required Result**                                         |
|---------------|-------------------------------------------------------------|
| Repository    | All placeholders replaced; secrets absent from Git history. |
| Local         | Frontend, backend and DB health pass.                       |
| Terraform     | fmt, validate and plan pass.                                |
| Network       | Only ALB and restricted Bastion are public.                 |
| Compute       | ASG instances healthy in private subnets.                   |
| Database      | RDS private, encrypted and reachable only from App SG.      |
| Storage       | S3 private, encrypted and versioned.                        |
| Application   | Registration, login, upload, download and delete pass.      |
| Lambda        | All three functions deployed and triggers configured.       |
| Security      | CloudTrail/EventBridge alerts verified.                     |
| Monitoring    | CloudWatch and Grafana data visible.                        |
| Notifications | SNS/Slack test successful.                                  |
| CI/CD         | GitHub Actions green.                                       |
| Cleanup       | Destroy procedure tested in sandbox.                        |
