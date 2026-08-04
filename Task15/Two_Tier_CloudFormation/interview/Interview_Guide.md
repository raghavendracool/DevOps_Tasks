# Task 15 — Interview Guide

## 1. What is AWS CloudFormation?

CloudFormation is an Infrastructure as Code service that provisions related AWS resources as a stack from a YAML or JSON template.

## 2. What is a stack?

A stack is the deployed collection of resources defined by a CloudFormation template.

## 3. Why use CloudFormation?

It provides repeatability, version control, dependency management, automated rollback and consistent environments.

## 4. Why does the ALB use two public subnets?

Application Load Balancers require subnets in at least two Availability Zones.

## 5. Why is the Web Server private?

It should receive HTTP only from the ALB and administration only through controlled paths.

## 6. Why is NAT Gateway required?

User Data installs NGINX from Ubuntu repositories, so the private Web Server requires outbound internet access.

## 7. What is User Data?

A startup script executed during the instance's initial boot to automate configuration.

## 8. What is `Fn::Sub`?

An intrinsic function that substitutes CloudFormation variables and resource attributes into strings.

## 9. What is `!Ref`?

It returns a parameter value or the primary identifier of a resource.

## 10. What is `!GetAtt`?

It returns a specific resource attribute such as an ALB DNS name or EC2 private IP.

## 11. Why use `DependsOn`?

It creates an explicit dependency when CloudFormation cannot infer the required order.

## 12. What is a CreationPolicy?

It allows CloudFormation to wait for a resource signal before considering resource creation successful.

## 13. What is `cfn-signal`?

A helper that signals successful or failed configuration back to CloudFormation.

## 14. Why use IMDSv2?

It requires session tokens and provides stronger EC2 metadata protection.

## 15. Why use Security Group references?

They restrict traffic by trusted tier rather than changing IP addresses.

## 16. Why use a Launch Template in production?

It supports Auto Scaling and provides a versioned reusable EC2 configuration.

## 17. What is a Change Set?

A preview of how a proposed template update will affect stack resources.

## 18. What is drift?

Drift occurs when deployed resources differ from the CloudFormation template due to out-of-band changes.

## 19. Why is `CAPABILITY_NAMED_IAM` required?

The template creates explicitly named IAM resources.

## 20. What happens when stack creation fails?

CloudFormation normally rolls back resources created during the failed deployment.
