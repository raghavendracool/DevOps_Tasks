# Part 2 — RDS MySQL Creation and Network Security

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Create the RDS Security Group

Create:

```text
Name: task11-rds-sg
VPC: Project VPC
```

Initial inbound rules for setup:

| Type | Port | Source |
|---|---:|---|
| MySQL/Aurora | 3306 | Your public IP `/32` temporarily |
| MySQL/Aurora | 3306 | `task11-web-sg` |

Do not use:

```text
0.0.0.0/0
```

for MySQL.

## Step 2 — Create a DB Subnet Group

Open:

```text
RDS → Subnet groups → Create DB subnet group
```

Select at least two private subnets in different Availability Zones.

Example:

```text
Private DB Subnet A → ap-south-1a
Private DB Subnet B → ap-south-1b
```

## Step 3 — Create the RDS MySQL Instance

Open:

```text
RDS → Databases → Create database
```

Configure:

```text
Creation method: Standard create
Engine: MySQL
Template: Free tier or Dev/Test for lab
DB instance identifier: task11-mysql-db
Master username: dbadmin
Credential management: Secrets Manager recommended
```

Training size example:

```text
DB instance class: db.t3.micro or currently available small burstable class
Storage: 20 GiB gp3
Storage autoscaling: Optional
```

Connectivity:

```text
VPC: Project VPC
DB subnet group: task11-db-subnet-group
Public access: No (recommended)
VPC Security Group: task11-rds-sg
Port: 3306
```

Additional configuration:

```text
Initial database name: Leave blank or use appdb
Automated backups: Enabled
Backup retention: 7 days for lab
Encryption: Enabled
Deletion protection: Enable for production
Performance Insights: Optional
Enhanced monitoring: Optional
```

## Local Workbench Connectivity Options

Because private RDS cannot be reached directly from the internet, use one of these:

### Option A — SSH Tunnel Through EC2

Preferred training approach.

MySQL Workbench connection method:

```text
Standard TCP/IP over SSH
SSH Hostname: <EC2_PUBLIC_IP>:22
SSH Username: ubuntu
SSH Key File: project-key.pem
MySQL Hostname: <RDS_ENDPOINT>
MySQL Server Port: 3306
Username: dbadmin
```

### Option B — Temporary Public RDS Access

Use only for a short lab:

- Set Publicly accessible to Yes
- Allow port 3306 only from your public IP
- Complete SQL setup
- Remove public access and public-IP rule afterward

## Step 4 — Record Connection Details

```text
Endpoint: task11-mysql-db.xxxxxx.ap-south-1.rds.amazonaws.com
Port: 3306
Master user: dbadmin
```

Do not store the master password in GitHub.

## Step 5 — Test from EC2

Install client:

```bash
sudo apt update
sudo apt install mysql-client -y
```

Connect:

```bash
mysql \
  -h <RDS_ENDPOINT> \
  -P 3306 \
  -u dbadmin \
  -p
```

## Checklist

- [ ] RDS Security Group created
- [ ] Private DB subnet group created
- [ ] RDS MySQL instance available
- [ ] Public access disabled or tightly temporary
- [ ] Encryption enabled
- [ ] Backup retention configured
- [ ] EC2-to-RDS port 3306 rule configured
- [ ] Endpoint recorded
