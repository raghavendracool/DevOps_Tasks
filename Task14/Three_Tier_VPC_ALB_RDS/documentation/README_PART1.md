# Part 1 — Introduction, Architecture and Prerequisites

[← Main README](../README.md) | [Next: Part 2 →](README_PART2.md)

## Objective

Build a secure three-tier architecture:

```text
Users
  ↓
Internet-facing ALB
  ↓
Private EC2 Application Tier
  ↓
Private Amazon RDS MySQL
```

Administration occurs through:

```text
Administrator
  ↓ SSH
Bastion Host
  ↓ SSH
Private EC2
```

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon VPC | Isolated network |
| Public Subnets | ALB, NAT Gateway and Bastion |
| Private App Subnets | Three EC2 application servers |
| Private DB Subnets | Amazon RDS |
| Internet Gateway | Public internet access |
| NAT Gateway | Outbound internet for private EC2 |
| Application Load Balancer | Public web entry point |
| Target Group | Private EC2 registration and health checks |
| Amazon EC2 | Application servers and Bastion |
| Amazon RDS MySQL | Private relational database |
| Security Groups | Tier-to-tier access control |
| CloudWatch | Metrics and logs |

## Architecture

![Task 14 Architecture](../infographic.png)

## Recommended CIDR Design

```text
VPC:                  10.0.0.0/16

Public Subnet A:      10.0.1.0/24
Public Subnet B:      10.0.2.0/24

Private App Subnet A: 10.0.11.0/24
Private App Subnet B: 10.0.12.0/24

Private DB Subnet A:  10.0.21.0/24
Private DB Subnet B:  10.0.22.0/24
```

## High Availability Design

- ALB spans two public subnets.
- Application EC2 instances are distributed across private subnets.
- RDS DB subnet group spans two private DB subnets.
- Multi-AZ RDS is recommended for production.
- A single NAT Gateway is acceptable for a lab; one per AZ is recommended for production resilience.

## Security Model

```text
Internet → ALB SG :80/:443
ALB SG → App SG :80
Bastion SG → App SG :22
App SG → RDS SG :3306
```

No direct public access is allowed to:

- Private EC2 instances
- RDS database

## Prerequisites

- AWS account
- Ubuntu EC2 key pair
- MySQL client
- AWS CLI
- Basic VPC, Linux, NGINX and MySQL knowledge
- Unique RDS identifier
- Strong database passwords

## Checklist

- [ ] Region selected
- [ ] Two Availability Zones available
- [ ] Key pair available
- [ ] CIDR plan reviewed
- [ ] NAT Gateway cost understood
- [ ] Security Group flow understood
