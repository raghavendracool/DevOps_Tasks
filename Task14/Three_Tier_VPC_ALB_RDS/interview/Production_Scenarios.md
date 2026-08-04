# Task 14 — Real-Time Production Scenarios

## Scenario 1 — ALB Returns 503

Check target health, NGINX, app service, port 80 Security Group and health path.

## Scenario 2 — One Target Is Unhealthy

SSH through Bastion or Session Manager, run local curl and review service logs.

## Scenario 3 — App Cannot Reach RDS

Check RDS SG source, endpoint, port 3306, credentials and DB state.

## Scenario 4 — Private EC2 Cannot Install Packages

Check NAT Gateway, private route table and DNS.

## Scenario 5 — RDS Becomes Public

Disable public accessibility, remove public SG rules and review CloudTrail.

## Scenario 6 — Bastion Is Compromised

Isolate it, rotate keys, inspect logs, replace from clean AMI and investigate downstream access.

## Scenario 7 — ALB Traffic Is Uneven

Review target health, slow requests, keep-alive behavior and application response time.

## Scenario 8 — RDS Connections Exhausted

Use pooling, reduce workers and consider RDS Proxy.

## Scenario 9 — One AZ Fails

ALB continues through healthy AZs; ensure app and NAT design are multi-AZ.

## Scenario 10 — NAT Gateway Fails

Use one NAT Gateway per AZ and AZ-specific private route tables.

## Scenario 11 — New EC2 Deployment Is Inconsistent

Use Launch Templates, immutable AMIs and automated configuration.

## Scenario 12 — Database Password Is Exposed

Rotate credentials, update Secrets Manager and redeploy.

## Scenario 13 — ALB Health Check Passes but App Is Broken

Use a deeper readiness endpoint that tests required dependencies carefully.

## Scenario 14 — HTTPS Is Required

Add ACM certificate, 443 listener and 80-to-443 redirect.

## Scenario 15 — SQL Injection Is Reported

Use parameterized queries, patch code, review logs and restrict DB privileges.

## Scenario 16 — Traffic Surges

Use Auto Scaling, caching, CloudFront and database scaling.

## Scenario 17 — NAT Costs Are High

Use VPC endpoints and reduce internet-bound traffic.

## Scenario 18 — Need Zero Bastion Architecture

Use Session Manager or EC2 Instance Connect Endpoint.

## Scenario 19 — RDS Failover Causes Errors

Use retry logic, pool pre-ping and RDS Proxy.

## Scenario 20 — Management Wants Disaster Recovery

Use snapshots, cross-region replicas or restore procedures, Route 53 and tested runbooks.
