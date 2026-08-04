# Part 5 — Verification, Troubleshooting, Cleanup and Production Recommendations

[← Part 4](README_PART4.md) | [Main README](../README.md)

## End-to-End Verification

### Public Access

Only this should be public:

```text
Application Load Balancer
```

Bastion is also public for administration in this lab, but restricted to your IP.

Private EC2 and RDS must not have public IPs or public accessibility.

### ALB

```bash
curl -I http://<ALB_DNS_NAME>
```

### Target Group

Expected:

```text
3 registered targets
3 healthy targets
```

### Private EC2

```bash
hostname
hostname -I
curl http://localhost/health
```

### RDS

```bash
nc -vz <RDS_ENDPOINT> 3306
```

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| ALB 503 | No healthy targets | Health path and SG |
| Target unhealthy | App/NGINX down | Local curl and logs |
| EC2 cannot install packages | NAT route issue | Private route table |
| EC2 cannot reach RDS | RDS SG | Source must be App SG |
| Bastion cannot SSH | SG or key | Source IP and key |
| App shows DB error | Credentials/schema | Environment file |
| One target never serves | Registration/AZ | Target Group |
| RDS publicly reachable | Public flag or SG | RDS configuration |

## Useful Logs

```bash
sudo journalctl -u task14-app -n 100 --no-pager
sudo tail -100 /var/log/nginx/error.log
sudo tail -100 /var/log/auth.log
```

## Production Recommendations

- Use HTTPS with ACM.
- Redirect HTTP to HTTPS.
- Use Auto Scaling instead of three manually managed EC2 instances.
- Use Launch Templates.
- Use Multi-AZ RDS.
- Use Secrets Manager for DB credentials.
- Use RDS Proxy.
- Use Session Manager instead of Bastion.
- Use WAF in front of the ALB.
- Enable ALB access logs.
- Enable VPC Flow Logs.
- Use CloudWatch alarms.
- Use one NAT Gateway per AZ for resilience.
- Deploy through Terraform or CloudFormation.
- Use immutable AMIs or CI/CD deployment.
- Add Route 53 and health checks.

## Cost Optimization

Largest recurring costs:

- NAT Gateway
- ALB
- RDS
- EC2 instances

Lab savings:

- Delete NAT after testing.
- Use small burstable instances.
- Stop non-RDS EC2 when idle.
- Delete ALB after verification.
- Delete RDS after final snapshot.
- Avoid unnecessary Elastic IPs.

## Cleanup Order

1. Delete ALB listeners and ALB.
2. Delete Target Group.
3. Terminate private EC2 instances.
4. Terminate Bastion Host.
5. Delete RDS after optional final snapshot.
6. Delete NAT Gateway.
7. Release Elastic IP.
8. Delete Security Groups.
9. Delete route tables.
10. Delete subnets.
11. Delete Internet Gateway.
12. Delete VPC.

## Final Checklist

- [ ] ALB public
- [ ] Private EC2 has no public IP
- [ ] RDS private
- [ ] Bastion restricted
- [ ] All targets healthy
- [ ] End-to-end DB flow works
- [ ] Resources cleaned up
