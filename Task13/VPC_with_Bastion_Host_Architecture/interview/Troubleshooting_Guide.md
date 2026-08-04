# Task 13 — Troubleshooting Guide

## SSH Flow

```text
Laptop
  ↓
Bastion public IP reachable?
  ↓
Bastion SG allows your IP?
  ↓
Public route reaches IGW?
  ↓
SSH service active?
  ↓
Private SG allows Bastion SG?
  ↓
Private EC2 SSH service active?
```

## Bastion Diagnostics

```bash
ip addr
ip route
sudo ss -lntp | grep ':22'
sudo systemctl status ssh
sudo tail -100 /var/log/auth.log
nc -vz <PRIVATE_EC2_IP> 22
```

## Private EC2 Diagnostics

```bash
ip addr
ip route
sudo systemctl status ssh
sudo tail -100 /var/log/auth.log
curl -I https://aws.amazon.com
```

## Common Root Causes

- SSH open to wrong source
- Public IP missing on Bastion
- Private EC2 accidentally assigned a public IP
- Incorrect subnet route-table association
- NAT Gateway unavailable
- Key mismatch
- Wrong Linux username
- NACL blocking ephemeral traffic
- Corporate firewall blocking SSH

## Production Improvements

- Systems Manager Session Manager
- EC2 Instance Connect Endpoint
- Multi-AZ access architecture
- VPC endpoints
- VPC Flow Logs
- CloudWatch Agent
- Hardened AMI
- No copied SSH keys
