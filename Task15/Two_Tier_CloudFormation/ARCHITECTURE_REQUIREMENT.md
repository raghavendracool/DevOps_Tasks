# Corrected Architecture Requirement

An internet-facing Application Load Balancer must use subnets in at least two Availability Zones.

## Final Task 15 Layout

```text
VPC: 10.0.0.0/16

Public Subnet A: 10.0.1.0/24
- ALB
- Bastion Host
- NAT Gateway

Public Subnet B: 10.0.2.0/24
- ALB

Private Subnet A: 10.0.11.0/24
- Private Web Server EC2
```

## Traffic Flow

```text
Internet
  ↓
ALB in Public Subnet A and Public Subnet B
  ↓
Private Web Server EC2
```

## Administration Flow

```text
Administrator
  ↓
Bastion Host in Public Subnet A
  ↓
Private Web Server EC2
```
