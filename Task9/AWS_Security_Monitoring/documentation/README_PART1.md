# Part 1 — Introduction, Architecture and Prerequisites

[← Main README](../README.md) | [Next: Part 2 →](README_PART2.md)

## Objective

Create an event-driven security monitoring solution that:

- Detects IAM `CreateUser` API calls
- Determines whether the creator is authorized
- Automatically invokes Lambda
- Sends a detailed Slack notification
- Logs delivery status in CloudWatch
- Supports verification with a controlled test user

## AWS Services Used

| Service | Purpose |
|---|---|
| AWS CloudTrail | Records IAM management API events |
| Amazon EventBridge | Matches `CreateUser` events |
| AWS Lambda | Evaluates and formats security alerts |
| AWS Secrets Manager | Stores Slack webhook securely |
| Amazon CloudWatch Logs | Stores Lambda logs and errors |
| AWS IAM | Controls Lambda permissions |
| Slack Incoming Webhook | Receives security alerts |

## Architecture

![Task 9 Architecture](../infographic.png)

## What Counts as Unauthorized?

This project uses an allow-list model.

Lambda checks the ARN of the identity that created the IAM user.

Example environment variable:

```text
AUTHORIZED_CREATOR_ARNS=arn:aws:iam::<ACCOUNT_ID>:user/admin-user,arn:aws:iam::<ACCOUNT_ID>:role/security-admin
```

If the event creator ARN is not on the allow list, the event is treated as unauthorized.

## Event Details Used

The Slack notification includes:

- New IAM username
- Creator ARN
- Creator type
- AWS account ID
- Event time
- AWS Region
- Source IP address
- User agent
- CloudTrail event ID
- Request parameters
- Whether the creator was authorized

## Prerequisites

- AWS account
- CloudTrail management events available
- Slack workspace permission to create an Incoming Webhook
- AWS permissions for Lambda, IAM, EventBridge, Secrets Manager and CloudWatch
- Test IAM permissions in a non-production environment
- AWS Region selected

## Naming Convention

| Resource | Name |
|---|---|
| Lambda | `task9-unauthorized-iam-user-alert` |
| IAM role | `task9-security-monitor-role` |
| Secret | `task9/slack-webhook-url` |
| EventBridge rule | `task9-detect-iam-user-creation` |
| Log group | `/aws/lambda/task9-unauthorized-iam-user-alert` |

## Checklist

- [ ] Slack channel selected
- [ ] Authorized creator ARNs identified
- [ ] Test environment available
- [ ] CloudTrail event flow understood
- [ ] Secret-storage approach understood
