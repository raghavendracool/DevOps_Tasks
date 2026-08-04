# Part 2 — VPC, Subnets, Gateways and Route Tables

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Open VPC Creation

Open:

```text
AWS Console → VPC → Your VPCs → Create VPC
```

Choose:

```text
Resources to create: VPC and more
```

## Step 2 — Configure the VPC

Use:

```text
Name tag auto-generation: task13
IPv4 CIDR block: 10.0.0.0/16
IPv6 CIDR block: No IPv6 CIDR block
Tenancy: Default
```

## Step 3 — Configure Availability Zones and Subnets

Use one Availability Zone for the assignment:

```text
Number of Availability Zones: 1
Number of public subnets: 1
Number of private subnets: 1
```

Example subnet CIDRs:

```text
Public subnet:  10.0.1.0/24
Private subnet: 10.0.2.0/24
```

## Step 4 — Configure NAT Gateway

For full private-instance outbound internet access:

```text
NAT gateways: In 1 AZ
```

For a lower-cost lab:

```text
NAT gateways: None
```

Without NAT, the private instance can still communicate with the Bastion Host through the VPC local route, but cannot download internet packages.

## Step 5 — VPC Endpoints

For this basic task:

```text
VPC endpoints: None
```

Production improvements may include interface endpoints for Systems Manager and a gateway endpoint for S3.

## Step 6 — DNS Settings

Enable:

```text
DNS hostnames: Enabled
DNS resolution: Enabled
```

## Step 7 — Create the VPC

Review and click:

```text
Create VPC
```

The **VPC and More** workflow creates:

- VPC
- Public subnet
- Private subnet
- Internet Gateway
- Public route table
- Private route table
- Optional NAT Gateway
- Route-table associations

## Step 8 — Verify Public Subnet

Open:

```text
VPC → Subnets → task13-public-subnet
```

Enable:

```text
Auto-assign public IPv4 address
```

Expected public route:

```text
0.0.0.0/0 → Internet Gateway
```

## Step 9 — Verify Private Subnet

Open:

```text
VPC → Subnets → task13-private-subnet
```

Ensure:

```text
Auto-assign public IPv4 address: Disabled
```

Expected private route with NAT:

```text
0.0.0.0/0 → NAT Gateway
```

## Step 10 — Verify NAT Gateway

If enabled:

```text
State: Available
Subnet: Public Subnet
Elastic IP: Assigned
```

The NAT Gateway must be in the public subnet and its route table must reach the Internet Gateway.

## Checklist

- [ ] VPC created
- [ ] Public subnet created
- [ ] Private subnet created
- [ ] Internet Gateway attached
- [ ] Public route table associated
- [ ] Private route table associated
- [ ] Public IP auto-assignment enabled only for public subnet
- [ ] NAT Gateway configured or intentionally omitted
