# Task 10 — Real-Time Production Scenarios

## Scenario 1 — Access Key Created but No Alert

Check CloudTrail event, EventBridge rule, Lambda target, permissions and SNS subscription.

## Scenario 2 — Bucket Deleted Outside us-east-1 Triggers Alert

Add region filtering in both EventBridge and Lambda.

## Scenario 3 — Duplicate Notifications

Store CloudTrail event IDs in DynamoDB with TTL.

## Scenario 4 — Access Key ID Appears in Logs

Mask the key ID and never log the secret access key.

## Scenario 5 — EventBridge Rule Is Disabled

Create a CloudWatch alarm or Config rule to monitor the rule state.

## Scenario 6 — SNS Email Not Received

Check confirmation status, spam filtering, topic policy and publish logs.

## Scenario 7 — Slack Returns 429

Queue alerts through SQS and retry with exponential backoff.

## Scenario 8 — Lambda Times Out

Reduce processing, avoid synchronous external dependencies and use asynchronous fan-out.

## Scenario 9 — IAM User Deletion Was Legitimate

Use actor allow lists and approved-change context before escalating severity.

## Scenario 10 — Attacker Creates Key and Deletes User

Correlate events by user, actor and time window.

## Scenario 11 — Bucket Deleted Before Alert Is Read

CloudTrail and archived event records preserve the evidence.

## Scenario 12 — Multiple Accounts Need Coverage

Use cross-account EventBridge routing to a central security account.

## Scenario 13 — Lambda Cannot Reach Slack

If inside a VPC, configure NAT and correct routes.

## Scenario 14 — Security Wants Auto-Remediation

Separate detection from remediation and require approval for destructive actions.

## Scenario 15 — Archive Bucket Write Fails

Check IAM, bucket policy, KMS permissions and bucket region.

## Scenario 16 — Event Pattern Matches Too Broadly

Use exact event source, event name, detail type and region filters.

## Scenario 17 — CloudTrail Lookup Shows Event but EventBridge Did Not Match

Test the event against the rule pattern and verify the correct event bus and region.

## Scenario 18 — Alert Contains Insufficient Context

Include source IP, actor ARN, request parameters, event time and CloudTrail event ID.

## Scenario 19 — High Event Volume

Use SQS buffering, batch processing and reserved concurrency.

## Scenario 20 — Management Wants Monthly Trends

Store structured findings in S3 or DynamoDB and query them with Athena or QuickSight.
