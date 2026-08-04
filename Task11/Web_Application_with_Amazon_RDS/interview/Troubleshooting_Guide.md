# Task 11 — Troubleshooting Guide

## Connection Path

```text
Application error
   ↓
RDS status Available?
   ↓
Endpoint resolves?
   ↓
TCP port 3306 reachable?
   ↓
RDS SG allows EC2 SG?
   ↓
Credentials correct?
   ↓
Database and grants exist?
   ↓
TLS CA valid?
```

## Useful Linux Commands

```bash
getent hosts <RDS_ENDPOINT>
nc -vz <RDS_ENDPOINT> 3306
sudo journalctl -u task11-rds-app -n 100
sudo tail -100 /var/log/nginx/error.log
```

## Useful MySQL Commands

```sql
SHOW DATABASES;
SHOW PROCESSLIST;
SHOW GRANTS FOR 'appuser'@'%';
SELECT VERSION();
SELECT CURRENT_USER();
```

## Common Root Causes

- Public/private routing misunderstanding
- Wrong Security Group source
- Incorrect endpoint
- Wrong password
- Missing database
- Missing grants
- TLS CA not installed
- Database unavailable
- Connection exhaustion

## Production Improvements

- Secrets Manager
- RDS Proxy
- Multi-AZ
- Automated backups
- Deletion protection
- TLS enforcement
- Alarms
- Query monitoring
- Read replicas
