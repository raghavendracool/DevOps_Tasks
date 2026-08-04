# Project 06 — AWS Lambda File Classification

![Task 6 Architecture](infographic.png)

This project automatically classifies files uploaded to Amazon S3.

- Files beginning with `fin_` are moved to `Finance/`
- All other files are moved to `Non-Finance/`
- Amazon S3 Event Notifications invoke AWS Lambda whenever a new object is uploaded
- Amazon CloudWatch captures logs and errors

## Documentation

1. [Part 1 — Introduction, Architecture and Prerequisites](documentation/README_PART1.md)
2. [Part 2 — S3 Bucket, Folder Design and Test Files](documentation/README_PART2.md)
3. [Part 3 — Lambda Function, IAM Role and Deployment](documentation/README_PART3.md)
4. [Part 4 — S3 Event Notification, Testing and Monitoring](documentation/README_PART4.md)
5. [Part 5 — Verification, Cleanup and Troubleshooting](documentation/README_PART5.md)

## Interview Preparation

- [Interview Guide](interview/Interview_Guide.md)
- [Production Scenarios](interview/Production_Scenarios.md)
- [AWS CLI Cheat Sheet](interview/AWS_CLI_CheatSheet.md)
- [Troubleshooting Guide](interview/Troubleshooting_Guide.md)

## Project Flow

```text
User uploads file to S3 incoming/
        ↓
S3 ObjectCreated event
        ↓
Lambda function is invoked
        ↓
Lambda reads object key
        ↓
Filename starts with fin_ ?
   ┌───────────────┴───────────────┐
   │                               │
  Yes                              No
   │                               │
Copy to Finance/             Copy to Non-Finance/
   │                               │
Delete original object from incoming/
        ↓
CloudWatch logs success or failure
```
