# Task 14 — Troubleshooting Guide

## User Request Path

```text
User
 ↓
ALB DNS resolves?
 ↓
ALB listener active?
 ↓
Target Group has healthy targets?
 ↓
App SG allows ALB SG?
 ↓
NGINX listening on 80?
 ↓
Gunicorn listening on 8000?
 ↓
Application healthy?
 ↓
RDS SG allows App SG?
```

## Useful Commands

```bash
sudo systemctl status nginx --no-pager
sudo systemctl status task14-app --no-pager
sudo journalctl -u task14-app -n 100 --no-pager
curl http://localhost/health
nc -vz <RDS_ENDPOINT> 3306
```

## Common Root Causes

- Wrong subnet route-table association
- App EC2 accidentally has public IP
- ALB SG not allowed by App SG
- Health check path mismatch
- NGINX proxy misconfiguration
- RDS SG source mismatch
- NAT Gateway unavailable
- Database credentials incorrect

## Production Improvements

- Auto Scaling Group
- Launch Template
- Session Manager
- HTTPS and ACM
- WAF
- Multi-AZ RDS
- Secrets Manager
- RDS Proxy
- CloudWatch alarms
- VPC Flow Logs
