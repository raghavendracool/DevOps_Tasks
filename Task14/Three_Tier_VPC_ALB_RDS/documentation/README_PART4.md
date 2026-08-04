# Part 4 — RDS, Application Deployment and Connectivity

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Step 1 — Create RDS MySQL

Configure:

```text
DB identifier: task14-mysql-db
Engine: MySQL
DB subnet group: task14-db-subnet-group
Public access: No
Security Group: task14-rds-sg
Encryption: Enabled
Backup retention: 7 days for lab
Multi-AZ: Recommended for production
```

Record:

```text
RDS endpoint
Port 3306
Master username
```

## Step 2 — Connect Through Bastion

Use ProxyJump from your local machine:

```bash
ssh \
  -i task14-key.pem \
  -J ubuntu@<BASTION_PUBLIC_IP> \
  ubuntu@<APP_PRIVATE_IP>
```

## Step 3 — Test RDS Network Access

From a private EC2 instance:

```bash
nc -vz <RDS_ENDPOINT> 3306
```

Install client if needed:

```bash
sudo apt update
sudo apt install mysql-client -y
```

Connect:

```bash
mysql \
  -h <RDS_ENDPOINT> \
  -u <MASTER_USER> \
  -p
```

## Step 4 — Create Database and User

Run:

```text
sql/01-create-database.sql
```

Creates:

```text
Database: appdb
User: appuser
```

The application user receives only required privileges.

## Step 5 — Configure Application Environment

On each EC2:

```bash
sudo nano /etc/task14-app.env
```

Add:

```text
DB_HOST=<RDS_ENDPOINT>
DB_PORT=3306
DB_NAME=appdb
DB_USER=appuser
DB_PASSWORD=<APP_DB_PASSWORD>
FLASK_SECRET_KEY=<LONG_RANDOM_VALUE>
INSTANCE_NAME=task14-app-01
```

Use a different `INSTANCE_NAME` on each server.

## Step 6 — Restart Application

```bash
sudo systemctl restart task14-app
sudo systemctl restart nginx
```

## Step 7 — Verify Local Application

```bash
curl http://localhost/health
curl http://localhost/api/db
```

Expected:

```json
{"status":"healthy"}
```

and successful DB connectivity.

## Step 8 — Verify Through ALB

Open:

```text
http://<ALB_DNS_NAME>
```

Refresh multiple times.

The page should display different instance names as the ALB distributes traffic.

## Step 9 — Verify Database Functionality

Register or submit a sample record through the application.

Then query RDS:

```sql
USE appdb;
SELECT * FROM visits ORDER BY created_at DESC;
```

## Checklist

- [ ] RDS created privately
- [ ] EC2 reaches RDS on port 3306
- [ ] Database created
- [ ] Restricted app user created
- [ ] All EC2 instances configured
- [ ] Health endpoint works
- [ ] ALB URL works
- [ ] Database writes verified
