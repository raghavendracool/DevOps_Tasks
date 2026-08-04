# Project 10 — CloudTrail Security Monitoring

![Task 10 Architecture](infographic.png)

This project detects and processes important AWS security events using CloudTrail, EventBridge and Lambda.

## Events Monitored

- IAM `CreateAccessKey`
- IAM `DeleteUser`
- Amazon S3 `DeleteBucket` in `us-east-1`

## Flow

```text
AWS API activity
      ↓
CloudTrail management event
      ↓
EventBridge rule
      ↓
Lambda security monitor
      ↓
CloudWatch Logs
      ↓
SNS alert and optional Slack notification
```

## Documentation

1. [Part 1 — Introduction, Architecture and Prerequisites](documentation/README_PART1.md)
2. [Part 2 — CloudTrail, SNS and Notification Setup](documentation/README_PART2.md)
3. [Part 3 — Lambda Code and IAM Permissions](documentation/README_PART3.md)
4. [Part 4 — EventBridge Rules and Testing](documentation/README_PART4.md)
5. [Part 5 — Verification, Troubleshooting and Cleanup](documentation/README_PART5.md)

## Interview Preparation

- [Interview Guide](interview/Interview_Guide.md)
- [Production Scenarios](interview/Production_Scenarios.md)
- [AWS CLI Cheat Sheet](interview/AWS_CLI_CheatSheet.md)
- [Troubleshooting Guide](interview/Troubleshooting_Guide.md)
