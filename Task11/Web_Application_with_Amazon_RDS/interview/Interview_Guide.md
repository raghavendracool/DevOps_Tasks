# Task 11 — Interview Guide

## 1. Explain the architecture.

The user reaches NGINX on EC2. NGINX forwards requests to Gunicorn and Flask. Flask uses a restricted MySQL user to connect over port 3306 to a private RDS instance.

## 2. Why use RDS instead of MySQL on EC2?

RDS manages backups, patching, monitoring, storage and high-availability options.

## 3. Why should RDS be private?

The database should be reachable only by approved application resources, not the public internet.

## 4. How should the RDS Security Group be configured?

Allow port 3306 only from the EC2 application Security Group.

## 5. Why create a separate application DB user?

It limits the application's privileges and avoids using the master user.

## 6. Why not store passwords in GitHub?

They can be exposed through repository history, logs or forks.

## 7. What is the recommended secret store?

AWS Secrets Manager or another approved secrets platform.

## 8. Why use TLS?

TLS protects credentials and queries in transit.

## 9. What is Multi-AZ?

RDS maintains a synchronous standby in another Availability Zone for failover.

## 10. What is the difference between Multi-AZ and a Read Replica?

Multi-AZ is mainly for availability; Read Replicas are mainly for read scaling.

## 11. What is RDS Proxy?

A managed proxy that pools connections and improves application resilience during failover.

## 12. Why use connection pooling?

It reduces connection setup overhead and prevents exhausting database connection limits.

## 13. How do you verify connectivity?

Test DNS, TCP 3306, MySQL authentication, TLS and an application query.

## 14. What causes `Access denied for user`?

Wrong username/password, host pattern, missing grants or authentication plugin mismatch.

## 15. How do automated backups work?

RDS creates backups and transaction logs that support point-in-time recovery within the retention window.

## 16. How do you monitor RDS?

CloudWatch metrics, Database Insights or Performance Insights, Enhanced Monitoring, slow-query logs and alarms.

## 17. How do you scale vertically?

Modify the DB instance class and storage.

## 18. How do you scale reads?

Use Read Replicas, caching and query optimization.

## 19. How do you prevent SQL injection?

Use ORM or parameterized queries, validate input and grant least privilege.

## 20. How do you deploy safely?

Use migrations, backups, health checks, rolling application deployment and rollback plans.
