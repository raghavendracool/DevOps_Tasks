# Task 9 — Real-Time Production Scenarios

## Scenario 1 — IAM User Was Created but Lambda Did Not Run

Check:

- EventBridge rule enabled
- Event pattern exact match
- Correct event bus
- Lambda target configured
- EventBridge permission to invoke Lambda
- CloudTrail event exists

## Scenario 2 — Authorized Admin Is Alerted

The actual identity may be an STS assumed-role ARN.

Update the allow list with a wildcard assumed-role pattern.

## Scenario 3 — Slack Receives No Message

Check:

- Secret value
- Secret IAM permission
- Slack webhook validity
- Lambda internet access
- Slack HTTP status in CloudWatch

## Scenario 4 — Lambda Is in a Private Subnet

Provide:

- NAT Gateway for Slack access
- Secrets Manager VPC endpoint
- Correct routes and Security Groups

## Scenario 5 — Duplicate Slack Alerts

Use CloudTrail `eventID` as an idempotency key in DynamoDB.

## Scenario 6 — Attacker Creates User and Access Key Immediately

Add detection for:

- `CreateAccessKey`
- `CreateLoginProfile`
- `AttachUserPolicy`
- `PutUserPolicy`
- Group membership changes

Correlate events by username and time window.

## Scenario 7 — Slack Webhook Is Exposed

Revoke the webhook immediately, create a new one, update Secrets Manager and investigate CloudTrail access to the secret.

## Scenario 8 — CloudTrail Event Is Delayed

Compare event time and Lambda receipt time. Maintain a backup scheduled query or Security Hub control for critical detections.

## Scenario 9 — Service Creates an IAM User

Review `userIdentity.type`, `invokedBy`, session context and approved automation roles before classifying.

## Scenario 10 — Security Team Wants Automatic Deletion

Do not immediately delete the user without context.

Safer response:

- Disable login profile
- Deactivate access keys
- Detach high-risk policies
- Open incident
- Require approval

## Scenario 11 — Slack Is Not an Approved Security System

Send findings to SNS, Security Hub, SQS, PagerDuty, Teams or a SIEM.

## Scenario 12 — Account Has Multiple Admin Roles

Manage authorized patterns in Parameter Store, DynamoDB or AppConfig instead of a long environment variable.

## Scenario 13 — False Positive from CI/CD

Approve only the specific pipeline role and monitor source account, session issuer and repository context.

## Scenario 14 — Lambda Logs Contain Sensitive Data

Avoid logging full request payloads when unnecessary and redact credential-like fields.

## Scenario 15 — Unauthorized User Was Created in Another Account

Use Organizations and cross-account EventBridge routing to a centralized security account.

## Scenario 16 — Slack Returns HTTP 429

Implement retry with backoff and queue alerts through SQS.

## Scenario 17 — EventBridge Target Delivery Fails

Configure a dead-letter queue on the EventBridge target and monitor failed invocations.

## Scenario 18 — User Is Created and Deleted Before Investigation

CloudTrail remains the audit record. Preserve logs and include event IDs in the alert.

## Scenario 19 — Security Wants Severity Levels

Classify severity using creator trust, source IP, account type, policy attachment and time of day.

## Scenario 20 — Compliance Requires Proof of Delivery

Record Slack HTTP status, request ID and delivery timestamp in CloudWatch or DynamoDB.
