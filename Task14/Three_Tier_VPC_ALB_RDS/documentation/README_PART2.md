# Part 2 — VPC, Subnets, Gateways and Route Tables

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Create the VPC

Open:

```text
VPC → Your VPCs → Create VPC
```

Choose:

```text
Resources to create: VPC and more
```

Configure:

```text
Name: task14
IPv4 CIDR: 10.0.0.0/16
Availability Zones: 2
Public subnets: 2
Private subnets: 4
NAT gateways: 1 per AZ for production or 1 total for lab
VPC endpoints: None initially
DNS hostnames: Enabled
DNS resolution: Enabled
```

## Step 2 — Identify Subnet Roles

Rename subnets:

```text
task14-public-a
task14-public-b
task14-app-private-a
task14-app-private-b
task14-db-private-a
task14-db-private-b
```

## Step 3 — Public Route Table

Associate with both public subnets.

Routes:

```text
10.0.0.0/16 → local
0.0.0.0/0   → Internet Gateway
```

## Step 4 — Private Application Route Table

Associate with both application private subnets.

Routes:

```text
10.0.0.0/16 → local
0.0.0.0/0   → NAT Gateway
```

The NAT Gateway lets private EC2 install packages and pull updates without becoming publicly reachable.

## Step 5 — Private Database Route Table

Associate with both DB private subnets.

Recommended:

```text
10.0.0.0/16 → local
```

RDS normally does not require outbound internet access.

## Step 6 — Verify Public IP Assignment

Public subnets:

```text
Auto-assign public IPv4: Enabled
```

Private subnets:

```text
Auto-assign public IPv4: Disabled
```

## Step 7 — Create DB Subnet Group

Open:

```text
RDS → Subnet groups → Create DB subnet group
```

Select:

```text
task14-db-private-a
task14-db-private-b
```

## Checklist

- [ ] VPC created
- [ ] Two public subnets configured
- [ ] Two private app subnets configured
- [ ] Two private DB subnets configured
- [ ] IGW attached
- [ ] NAT Gateway available
- [ ] Route tables associated correctly
- [ ] DB subnet group created
