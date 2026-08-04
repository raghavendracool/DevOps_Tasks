# Task 9 — Interview Guide

## 1. Explain the architecture.

CloudTrail records IAM `CreateUser`. EventBridge matches the event and invokes Lambda. Lambda checks the creator ARN against an allow list, reads the Slack webhook from Secrets Manager, posts the alert and logs delivery in CloudWatch.

## 2. Why use EventBridge instead of polling CloudTrail?

EventBridge provides near-real-time event routing without running scheduled scans.

## 3. Why store the webhook in Secrets Manager?

The Slack webhook is a credential-like secret and should not be committed to code or stored as plaintext configuration.

## 4. How do you define unauthorized?

By comparing the creator identity ARN with an approved allow list.

## 5. Why can assumed-role ARNs complicate the allow list?

The event may contain an STS session ARN instead of the IAM role ARN.

## 6. How do you support assumed roles?

Use wildcard patterns such as:

```text
arn:aws:sts::<ACCOUNT_ID>:assumed-role/security-admin/*
```

## 7. What details should be in the alert?

Username, creator, identity type, account, region, source IP, event time, event ID and user agent.

## 8. What if Slack is unavailable?

Lambda should fail, retry and send the event to an SQS dead-letter queue or failure destination.

## 9. How do you avoid duplicate alerts?

Store CloudTrail event IDs in DynamoDB with TTL and skip already processed IDs.

## 10. Is IAM regional?

IAM is global, but CloudTrail events include an AWS region field and are delivered through regional EventBridge infrastructure.

## 11. Why log the Slack status?

It proves whether the webhook accepted the notification.

## 12. How do you test safely?

Use a non-production account, create a clearly named temporary user, verify the alert and delete the user.

## 13. What if the creator is an AWS service?

Inspect `userIdentity.type`, `invokedBy`, session issuer and source details.

## 14. How would you detect access-key creation?

Add `CreateAccessKey` to a separate EventBridge rule or event-name list.

## 15. How would you centralize this across accounts?

Use AWS Organizations, cross-account event buses and a central security account.

## 16. How would you send findings to Security Hub?

Use `BatchImportFindings` with the AWS Security Finding Format.

## 17. Why use least privilege?

The Lambda only needs logging and access to one Slack secret.

## 18. How do you monitor the monitor?

CloudWatch alarms for Lambda Errors, Throttles and Duration plus a failure destination.

## 19. What is the risk of hardcoding an admin username?

Names can change, roles may be assumed and federated identities may not map cleanly. ARN-based patterns are safer.

## 20. How do you improve the alert?

Add severity, environment, owner, response links, runbook URL and an automated ticket.
