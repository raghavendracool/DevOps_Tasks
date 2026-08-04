# Project 07 — AWS Compliance Monitoring

![Task 7 Architecture](infographic.png)

This project uses AWS Lambda to continuously monitor an AWS account for compliance.

## Compliance Rules

- Every EC2 instance must contain the required tags.
- Every EBS volume must be encrypted.
- Active IAM access keys must be rotated within two days.
- Non-compliant resources are written to CloudWatch Logs.
- An optional Amazon SNS notification is published when violations are found.
- Lambda timeout is configured as **30 seconds**.

## Documentation

1. [Part 1 — Introduction, Architecture and Prerequisites](documentation/README_PART1.md)
2. [Part 2 — IAM Role, SNS Topic and Lambda Configuration](documentation/README_PART2.md)
3. [Part 3 — Compliance Lambda Code and Rules](documentation/README_PART3.md)
4. [Part 4 — EventBridge Schedule, Testing and Monitoring](documentation/README_PART4.md)
5. [Part 5 — Verification, Cleanup and Troubleshooting](documentation/README_PART5.md)

## Interview Preparation

- [Interview Guide](interview/Interview_Guide.md)
- [Production Scenarios](interview/Production_Scenarios.md)
- [AWS CLI Cheat Sheet](interview/AWS_CLI_CheatSheet.md)
- [Troubleshooting Guide](interview/Troubleshooting_Guide.md)

## Project Flow

```text
EventBridge Scheduler
        ↓
Lambda Compliance Monitor
        ↓
 ┌───────────────┬────────────────┬─────────────────────┐
 │               │                │
EC2 Tags      EBS Encryption   IAM Access-Key Age
 │               │                │
 └───────────────┴────────────────┴─────────────────────┘
        ↓
Structured Compliance Report
        ↓
CloudWatch Logs
        ↓
SNS Alert when violations exist
```
