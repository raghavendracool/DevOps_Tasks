# Task 11 — AWS CLI Cheat Sheet

## Describe RDS

```bash
aws rds describe-db-instances \
  --db-instance-identifier task11-mysql-db
```

## Get Endpoint

```bash
aws rds describe-db-instances \
  --db-instance-identifier task11-mysql-db \
  --query 'DBInstances[0].Endpoint'
```

## Check Public Accessibility

```bash
aws rds describe-db-instances \
  --db-instance-identifier task11-mysql-db \
  --query 'DBInstances[0].PubliclyAccessible'
```

## Modify Public Access

```bash
aws rds modify-db-instance \
  --db-instance-identifier task11-mysql-db \
  --no-publicly-accessible \
  --apply-immediately
```

## Create Snapshot

```bash
aws rds create-db-snapshot \
  --db-instance-identifier task11-mysql-db \
  --db-snapshot-identifier task11-final-snapshot
```

## MySQL Connectivity

```bash
mysql \
  --ssl-mode=VERIFY_IDENTITY \
  --ssl-ca=/etc/ssl/certs/global-bundle.pem \
  -h <RDS_ENDPOINT> \
  -u appuser \
  -p appdb
```
