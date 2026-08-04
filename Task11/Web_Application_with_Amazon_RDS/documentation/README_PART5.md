# Part 5 — Verification, Troubleshooting, Cleanup and Production Recommendations

[← Part 4](README_PART4.md) | [Main README](../README.md)

## End-to-End Verification

### From EC2

```bash
nc -vz <RDS_ENDPOINT> 3306

mysql \
  --ssl-mode=VERIFY_IDENTITY \
  --ssl-ca=/etc/ssl/certs/global-bundle.pem \
  -h <RDS_ENDPOINT> \
  -u appuser \
  -p appdb
```

### Application

```bash
sudo systemctl status task11-rds-app --no-pager
sudo journalctl -u task11-rds-app -n 100 --no-pager
sudo systemctl status nginx --no-pager
curl -I http://localhost
```

### Database

```sql
USE appdb;

SELECT id, username, created_at
FROM users
ORDER BY created_at DESC;
```

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| Connection timeout | SG, route or subnet | Port 3306 and network |
| Access denied | Wrong DB credentials | User and grants |
| Unknown database | DB not created | `SHOW DATABASES` |
| NGINX 502 | Gunicorn down | systemd logs |
| TLS failure | Missing CA bundle | SSL configuration |
| Login always fails | Hash/query issue | App logs and DB row |
| Too many connections | Pooling issue | MySQL connections |
| Workbench cannot connect | Private RDS | SSH tunnel |

## Production Recommendations

### Credentials

Use AWS Secrets Manager to store and rotate DB credentials. Amazon RDS can integrate with Secrets Manager for master-user password management. citeturn601552search6

### Network Security

Keep RDS private and permit MySQL only from the application Security Group. AWS documentation recommends using Security Groups to control which EC2 instances or IPs can reach the database. citeturn601552search4turn601552search15

### Encryption

Enable RDS encryption at rest and require TLS for database connections. RDS handles encrypted-storage access transparently for applications. citeturn601552search7

### Connection Scalability

Use SQLAlchemy connection pooling and consider RDS Proxy for workloads with many or short-lived connections. RDS Proxy pools and shares database connections and improves resilience during failover. citeturn601552search12turn601552search19

### Authentication

For supported application patterns, IAM database authentication can avoid storing a long-lived database password in code by generating short-lived tokens. citeturn601552search22

### Availability

- Multi-AZ
- Automated backups
- Point-in-time recovery
- Deletion protection
- CloudWatch alarms
- Performance Insights or Database Insights
- Tested restoration procedure

## Cleanup

1. Stop the application.
2. Terminate EC2.
3. Delete Elastic IP if used.
4. Delete RDS after taking a final snapshot when needed.
5. Delete manual snapshots not required.
6. Delete DB subnet group.
7. Delete Security Groups.
8. Delete Secrets Manager secrets if no longer required.
9. Delete CloudWatch log groups.
10. Confirm no RDS Proxy remains.

## Final Checklist

- [ ] RDS MySQL available
- [ ] Workbench connection verified
- [ ] Database and restricted user created
- [ ] Application connected with app credentials
- [ ] Registration succeeded
- [ ] Login succeeded
- [ ] RDS is private after setup
- [ ] Port 3306 is not public
- [ ] Credentials are not in GitHub
