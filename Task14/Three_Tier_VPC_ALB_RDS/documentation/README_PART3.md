# Part 3 — Security Groups, Bastion, ALB and EC2

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Step 1 — Create ALB Security Group

```text
Name: task14-alb-sg
```

Inbound:

| Type | Port | Source |
|---|---:|---|
| HTTP | 80 | `0.0.0.0/0` |
| HTTPS | 443 | `0.0.0.0/0` when configured |

## Step 2 — Create Bastion Security Group

```text
Name: task14-bastion-sg
```

Inbound:

| Type | Port | Source |
|---|---:|---|
| SSH | 22 | Your public IP `/32` |

## Step 3 — Create Application Security Group

```text
Name: task14-app-sg
```

Inbound:

| Type | Port | Source |
|---|---:|---|
| HTTP | 80 | `task14-alb-sg` |
| SSH | 22 | `task14-bastion-sg` |

## Step 4 — Create RDS Security Group

```text
Name: task14-rds-sg
```

Inbound:

| Type | Port | Source |
|---|---:|---|
| MySQL/Aurora | 3306 | `task14-app-sg` |

## Step 5 — Launch Bastion Host

```text
AMI: Ubuntu Server 24.04 LTS
Subnet: task14-public-a
Public IP: Enabled
Security Group: task14-bastion-sg
```

## Step 6 — Launch Three Private EC2 Instances

Launch:

```text
task14-app-01 → task14-app-private-a
task14-app-02 → task14-app-private-b
task14-app-03 → task14-app-private-a or B
```

Configure:

```text
AMI: Ubuntu Server 24.04 LTS
Instance type: t3.micro
Public IP: Disabled
Security Group: task14-app-sg
```

Use the supplied script:

```text
scripts/app-user-data.sh
```

It installs:

- NGINX
- Python
- Flask dependencies
- Gunicorn
- MySQL client
- Sample application files

## Step 7 — Create Target Group

```text
Target type: Instances
Protocol: HTTP
Port: 80
Health check path: /health
```

Register all three private EC2 instances.

## Step 8 — Create ALB

```text
Name: task14-alb
Scheme: Internet-facing
Subnets: task14-public-a and task14-public-b
Security Group: task14-alb-sg
Listener: HTTP 80
Target Group: task14-app-tg
```

Wait until:

```text
ALB state: Active
Targets: Healthy
```

## Checklist

- [ ] ALB SG created
- [ ] Bastion SG created
- [ ] App SG created
- [ ] RDS SG created
- [ ] Bastion launched publicly
- [ ] Three EC2 instances launched privately
- [ ] Target Group created
- [ ] All targets healthy
- [ ] ALB created in two public subnets
