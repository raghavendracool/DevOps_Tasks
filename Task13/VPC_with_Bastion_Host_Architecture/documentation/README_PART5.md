# Part 5 — Troubleshooting, Cleanup and Production Recommendations

[← Part 4](README_PART4.md) | [Main README](../README.md)

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| Cannot reach Bastion | SG or public route | Port 22, IGW, public IP |
| Bastion connects but private fails | Private SG | Source must be Bastion SG |
| `Permission denied` | Key or user issue | Key permissions and Ubuntu user |
| Private EC2 has no internet | NAT or route issue | Private route and NAT state |
| NAT does not work | NAT in wrong subnet | Public subnet and IGW route |
| ProxyJump fails | SSH syntax/config | Bastion hostname and key |
| Connection timeout | NACL or route | Subnet NACL and local route |
| DNS fails privately | VPC DNS disabled | DNS support and hostnames |

## Useful Diagnostics

### Local Machine

```bash
ssh -vvv \
  -i task13-key.pem \
  ubuntu@<BASTION_PUBLIC_IP>
```

### Bastion

```bash
nc -vz <PRIVATE_EC2_IP> 22
ip route
sudo ss -lntp | grep ':22'
```

### Private EC2

```bash
ip addr
ip route
sudo systemctl status ssh --no-pager
sudo tail -100 /var/log/auth.log
```

## Network ACL Notes

Default Network ACLs allow traffic.

If using custom NACLs, allow:

- Inbound SSH port 22 where required
- Outbound ephemeral ports
- Return traffic
- NAT and internet response flows

Security Groups are stateful. NACLs are stateless.

## Production Recommendations

### Prefer Systems Manager Session Manager

Modern AWS environments often use Session Manager instead of a public Bastion Host.

Benefits:

- No inbound SSH port
- No public IP
- IAM-based access
- Central audit logging
- Session recording
- No key-pair distribution

Recommended design:

```text
Administrator
    ↓ IAM
Systems Manager Session Manager
    ↓
Private EC2
```

Private instances can use interface VPC endpoints for:

```text
ssm
ssmmessages
ec2messages
```

### Bastion Hardening

When a Bastion Host is required:

- Use a minimal hardened AMI.
- Restrict SSH source to approved CIDRs.
- Use MFA-backed identity controls.
- Patch automatically.
- Enable CloudWatch and audit logs.
- Rotate or avoid static keys.
- Use Auto Scaling and multiple AZs for high availability.
- Use an NLB only when architecture requires it.
- Remove unnecessary packages and outbound access.
- Enable GuardDuty and Inspector.

### Cost Optimization

NAT Gateway is usually the largest cost in this lab.

Lower-cost options:

- Omit NAT for a pure SSH demonstration.
- Use VPC endpoints for AWS services.
- Stop EC2 instances after testing.
- Use Session Manager instead of Bastion and NAT where possible.
- Delete unused Elastic IPs.

## Cleanup Order

1. Terminate private EC2.
2. Terminate Bastion Host.
3. Delete NAT Gateway.
4. Release NAT Elastic IP.
5. Delete Security Groups.
6. Delete custom route tables.
7. Delete subnets.
8. Detach and delete Internet Gateway.
9. Delete VPC.
10. Delete VPC Flow Log resources if created.

## Final Checklist

- [ ] Bastion removed after lab
- [ ] Private EC2 removed
- [ ] NAT Gateway deleted
- [ ] Elastic IP released
- [ ] Security Groups deleted
- [ ] VPC deleted
- [ ] No chargeable resources remain
