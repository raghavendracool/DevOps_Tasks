# Part 1 — Introduction, Architecture and Prerequisites

[← Main README](../README.md) | [Next: Part 2 →](README_PART2.md)

## Objective

Build a secure network architecture where a private EC2 instance does not have a public IP address and can only be accessed through a Bastion Host.

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon VPC | Isolated virtual network |
| Public Subnet | Hosts the Bastion Host |
| Private Subnet | Hosts the private EC2 instance |
| Internet Gateway | Internet access for the public subnet |
| NAT Gateway | Optional outbound internet for private EC2 |
| Route Tables | Control subnet routing |
| Security Groups | Stateful instance-level firewall |
| Amazon EC2 | Bastion and private instances |
| Elastic IP | Stable public IP for NAT or Bastion |
| CloudWatch | Monitoring and logs |
| VPC Flow Logs | Network traffic visibility |
| Systems Manager | Recommended modern alternative to Bastion |

## Architecture

![Task 13 Architecture](../infographic.png)

## Recommended CIDR Design

```text
VPC CIDR:          10.0.0.0/16
Public Subnet:     10.0.1.0/24
Private Subnet:    10.0.2.0/24
```

## Route Design

### Public Route Table

```text
10.0.0.0/16 → local
0.0.0.0/0   → Internet Gateway
```

### Private Route Table

With NAT Gateway:

```text
10.0.0.0/16 → local
0.0.0.0/0   → NAT Gateway
```

Without NAT Gateway:

```text
10.0.0.0/16 → local
```

## Security Model

- Bastion Host has a public IP.
- Bastion Security Group allows SSH only from your public IP.
- Private EC2 has no public IP.
- Private EC2 Security Group allows SSH only from the Bastion Security Group.
- The same key pair may be used for training, but separate controls are preferable in production.
- Password authentication remains disabled.

## Prerequisites

- AWS account
- EC2 key pair
- Your current public IP address
- SSH client
- AWS Region selected
- Basic Linux and networking knowledge

## Recommended Region

```text
ap-south-1
```

## Naming Convention

| Resource | Name |
|---|---|
| VPC | `task13-vpc` |
| Public Subnet | `task13-public-subnet` |
| Private Subnet | `task13-private-subnet` |
| Internet Gateway | `task13-igw` |
| NAT Gateway | `task13-nat-gateway` |
| Public Route Table | `task13-public-rt` |
| Private Route Table | `task13-private-rt` |
| Bastion Security Group | `task13-bastion-sg` |
| Private EC2 Security Group | `task13-private-sg` |
| Bastion Host | `task13-bastion-host` |
| Private EC2 | `task13-private-ec2` |

## Checklist

- [ ] Region selected
- [ ] Key pair available
- [ ] Public IP identified
- [ ] CIDR ranges confirmed
- [ ] NAT Gateway cost understood
- [ ] Bastion security model understood
