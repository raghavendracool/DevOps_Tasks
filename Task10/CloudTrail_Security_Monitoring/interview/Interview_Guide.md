# Task 10 — Interview Guide

## 1. Explain the architecture.

CloudTrail records API activity. EventBridge matches selected security events and invokes Lambda. Lambda parses the event, assigns severity, logs it, sends notifications and optionally archives it.

## 2. Why use separate EventBridge rules?

IAM events and the us-east-1-specific S3 event have different filters, making separate rules easier to understand and manage.

## 3. Why is `CreateAccessKey` high risk?

It creates a long-term programmatic credential that may be used outside AWS.

## 4. Why is `DeleteUser` important?

It may be legitimate administration or an attacker removing an identity or evidence.

## 5. Why is `DeleteBucket` critical?

It can indicate destructive activity and possible data loss.

## 6. How is us-east-1 filtering enforced?

Both EventBridge and Lambda validate the region.

## 7. Why double-check in Lambda?

It provides defense in depth if the EventBridge pattern is changed incorrectly.

## 8. How do you prevent secret exposure?

Mask access-key IDs and never log secret access-key values.

## 9. How do you handle duplicate events?

Use CloudTrail event ID as an idempotency key in DynamoDB.

## 10. How do you verify delivery?

Check Lambda logs, SNS delivery, Slack response status and event IDs.

## 11. Why use CloudWatch Logs?

They provide a searchable execution and evidence trail.

## 12. How would you integrate with a SIEM?

Forward through Kinesis Firehose, EventBridge, S3, Security Hub or a vendor connector.

## 13. How would you centralize across accounts?

Use AWS Organizations and cross-account EventBridge buses.

## 14. How would you reduce alert noise?

Use actor allow lists, account context, time windows and severity rules.

## 15. How do you test safely?

Use temporary resources in a sandbox and clean them immediately.

## 16. What if an S3 bucket is not empty?

`DeleteBucket` fails, so no successful deletion event occurs.

## 17. What if Slack is unavailable?

Use SNS/SQS fallback and retry with backoff.

## 18. How do you secure the Lambda role?

Allow only publishing, specific secret retrieval and optional archive writes.

## 19. How do you add more events?

Extend EventBridge patterns and the supported-event mapping.

## 20. How would you improve response automation?

Create Security Hub findings, tickets and approval-controlled remediation.
