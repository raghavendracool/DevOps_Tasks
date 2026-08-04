# 3. Architecture and Networking

## VPC Layout

```text
VPC: 10.0.0.0/16

Public Subnet A:  10.0.1.0/24
Public Subnet B:  10.0.2.0/24

App Private A:    10.0.11.0/24
App Private B:    10.0.12.0/24

DB Private A:     10.0.21.0/24
DB Private B:     10.0.22.0/24
```

## Resource Placement

| Resource | Placement |
|---|---|
| ALB | Public A and Public B |
| NAT Gateway | Public A for lab; one per AZ for production |
| Bastion | Public A |
| EC2 ASG | App Private A and B |
| RDS | DB Private A and B |
| S3/Lambda/CloudWatch | Regional managed services |

## Security Group Flow

```text
Internet → ALB SG :80/:443
ALB SG → App SG :80
Bastion SG → App SG :22
App SG → RDS SG :3306
```

## Public Exposure

Public:

- ALB
- Optional Bastion restricted to administrator IP

Private:

- EC2 application instances
- RDS
- S3 bucket
- Secrets

## High Availability

- ALB spans two Availability Zones
- Auto Scaling Group uses two private subnets
- RDS uses a multi-subnet DB subnet group
- Multi-AZ RDS recommended
- Health checks remove failed instances
- Auto Scaling replaces unhealthy instances
