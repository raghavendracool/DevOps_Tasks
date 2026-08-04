# Real-Time Production Scenarios

## ALB Returns 503

Check target health, Security Groups, application container, NGINX, and `/health`.

## Upload Works but Classification Does Not

Check S3 event notification, Lambda permission, prefix filters, logs, and destination key logic.

## App Cannot Connect to RDS

Check RDS state, DNS, App SG to RDS SG on 3306, credentials, and database existence.

## Security Alert Missing

Check CloudTrail event, EventBridge pattern, Lambda invocation, SNS subscription, and Slack secret.

## Compliance Scan Times Out

Split regions and checks, use Step Functions or SQS, and publish partial-scan metrics.

## High Traffic

Scale EC2 ASG, add CloudFront, cache data, use RDS Proxy, and review database indexes.

## One AZ Fails

ALB routes to healthy targets in the other AZ. Ensure app instances and NAT design are multi-AZ.

## Credentials Exposed

Rotate immediately, update Secrets Manager, redeploy, and investigate CloudTrail.

## S3 File Deleted Accidentally

Restore an earlier version using S3 Versioning.

## RDS Failure

Use Multi-AZ failover, connection retries, RDS Proxy, and point-in-time recovery.
