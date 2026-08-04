# Mega Project Interview Guide

## Explain the project in 90 seconds

I built SecureCloudOps Portal, a highly available three-tier AWS application. A React frontend and FastAPI backend run on private EC2 instances managed by an Auto Scaling Group behind an Application Load Balancer. Amazon RDS MySQL stores user and file metadata, while a private S3 bucket stores uploaded documents. S3 events invoke Lambda to classify finance and non-finance files. CloudTrail and EventBridge trigger security-monitoring Lambda functions, and a scheduled compliance Lambda publishes custom CloudWatch metrics displayed in Grafana. Infrastructure is provisioned with Terraform, with a CloudFormation example, and CI validation runs through GitHub Actions.

## Key Questions

1. Why are EC2 and RDS private?
2. Why does ALB require two public subnets?
3. How does Auto Scaling work?
4. Why use RDS instead of MySQL on EC2?
5. Why use presigned S3 URLs?
6. How does Lambda avoid recursive S3 triggers?
7. How are secrets managed?
8. How are IAM permissions restricted?
9. How do CloudTrail and EventBridge work together?
10. What custom CloudWatch metrics are published?
11. How does Grafana query CloudWatch?
12. What happens when one EC2 instance fails?
13. How do you test scale-out?
14. How do you prevent public S3 access?
15. What is the disaster-recovery plan?
16. How would you improve multi-region resilience?
17. Why use Terraform and CloudFormation?
18. How is deployment validated?
19. What are the largest costs?
20. How would you convert this to containers on ECS/EKS?
