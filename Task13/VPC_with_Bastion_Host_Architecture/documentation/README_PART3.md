# Part 3 — Security Groups and EC2 Deployment

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Step 1 — Create Bastion Security Group

Create:

```text
Name: task13-bastion-sg
VPC: task13-vpc
```

Inbound:

| Type | Port | Source |
|---|---:|---|
| SSH | 22 | Your public IP `/32` |

Outbound:

```text
All traffic → 0.0.0.0/0
```

Do not allow SSH from `0.0.0.0/0`.

## Step 2 — Create Private EC2 Security Group

Create:

```text
Name: task13-private-sg
VPC: task13-vpc
```

Inbound:

| Type | Port | Source |
|---|---:|---|
| SSH | 22 | `task13-bastion-sg` |

This Security Group chaining ensures only the Bastion Host can initiate SSH to the private instance.

## Step 3 — Launch Bastion Host

Configure:

```text
Name: task13-bastion-host
AMI: Ubuntu Server 24.04 LTS
Instance type: t3.micro
Key pair: Your EC2 key pair
VPC: task13-vpc
Subnet: task13-public-subnet
Auto-assign Public IP: Enabled
Security Group: task13-bastion-sg
Storage: 8 GiB gp3
```

## Step 4 — Launch Private EC2

Configure:

```text
Name: task13-private-ec2
AMI: Ubuntu Server 24.04 LTS
Instance type: t3.micro
Key pair: Same training key pair
VPC: task13-vpc
Subnet: task13-private-subnet
Auto-assign Public IP: Disabled
Security Group: task13-private-sg
Storage: 8 GiB gp3
```

## Step 5 — Record Addresses

Record:

```text
Bastion Public IP: <BASTION_PUBLIC_IP>
Bastion Private IP: <BASTION_PRIVATE_IP>
Private EC2 Private IP: <PRIVATE_EC2_IP>
```

## Step 6 — Verify Instance Placement

Bastion:

```text
Subnet: Public
Public IPv4: Present
Private IPv4: Present
```

Private EC2:

```text
Subnet: Private
Public IPv4: None
Private IPv4: Present
```

## Optional Hardening

For the Bastion Host:

- Install only required packages.
- Disable password authentication.
- Disable root SSH login.
- Use automatic patching.
- Enable CloudWatch Agent.
- Enable VPC Flow Logs.
- Use an Elastic IP only when a stable address is required.
- Restrict egress where practical.

## Checklist

- [ ] Bastion SG created
- [ ] SSH source restricted to your IP
- [ ] Private SG allows SSH only from Bastion SG
- [ ] Bastion launched in public subnet
- [ ] Bastion has public IP
- [ ] Private EC2 launched in private subnet
- [ ] Private EC2 has no public IP
