# Task 11 — Real-Time Production Scenarios

## Scenario 1 — Application Cannot Connect to RDS

Check DNS, Security Groups, routes, port 3306, credentials, DB status and TLS settings.

## Scenario 2 — MySQL Workbench Cannot Reach Private RDS

Use Standard TCP/IP over SSH through EC2 or a VPN/Direct Connect path.

## Scenario 3 — RDS CPU Is High

Check expensive queries, missing indexes, connection count, locks and workload changes.

## Scenario 4 — Too Many Connections

Use connection pooling, reduce worker connections and consider RDS Proxy.

## Scenario 5 — Login Is Slow

Inspect query latency, indexes on username, connection reuse and application logs.

## Scenario 6 — Database Password Was Exposed

Rotate the password, update Secrets Manager, redeploy the app and investigate access.

## Scenario 7 — RDS Fails Over

Connections may break. Use retry logic, pool pre-ping and RDS Proxy.

## Scenario 8 — Storage Is Almost Full

Enable storage autoscaling, clean data, archive old records and review growth.

## Scenario 9 — User Table Is Accidentally Deleted

Restore to a new RDS instance using point-in-time recovery, validate and cut over.

## Scenario 10 — Deployment Changes the Schema

Use versioned database migrations and backward-compatible releases.

## Scenario 11 — Unapproved Public RDS Access Is Found

Disable public access, remove public SG rules and review CloudTrail.

## Scenario 12 — Application Uses the Master User

Create a restricted app user, rotate master credentials and update the app.

## Scenario 13 — Read Traffic Increases

Add a Read Replica and direct read-only queries appropriately.

## Scenario 14 — Query Causes Locking

Inspect active transactions and lock waits; optimize transaction scope and indexes.

## Scenario 15 — RDS Certificate Changes

Use the current AWS CA bundle and test certificate rotation before enforcement.

## Scenario 16 — Secrets Manager Retrieval Adds Latency

Cache the secret in memory and retrieve it at startup or controlled refresh intervals.

## Scenario 17 — Multi-AZ Cost Is Questioned

Explain the availability benefit and compare it with business recovery requirements.

## Scenario 18 — Developer Needs Temporary DB Access

Use approved VPN, bastion, SSM port forwarding or SSH tunneling with time-bound access.

## Scenario 19 — SQL Injection Is Reported

Disable the vulnerable endpoint, use parameterized queries, review logs and rotate credentials if needed.

## Scenario 20 — Database Must Support More Application Instances

Use connection pooling, RDS Proxy, scalable instance sizing and load testing.
