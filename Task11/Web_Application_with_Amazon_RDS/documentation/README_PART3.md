# Part 3 — MySQL Workbench and SQL Configuration

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Step 1 — Install MySQL Workbench

Download MySQL Workbench for your operating system.

Create a connection using either:

```text
Standard TCP/IP over SSH
```

or temporary direct TCP/IP access.

## Step 2 — Test the Connection

Use:

```text
Hostname: <RDS_ENDPOINT>
Port: 3306
Username: dbadmin
Password: Master password
```

Click:

```text
Test Connection
```

Expected:

```text
Successfully made the MySQL connection
```

## Step 3 — Create Database and Application User

Run the supplied file:

```text
sql/01-create-database-and-user.sql
```

Update the application password before running.

Core SQL:

```sql
CREATE DATABASE appdb
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'appuser'@'%'
  IDENTIFIED BY 'REPLACE_WITH_STRONG_PASSWORD';

GRANT SELECT, INSERT, UPDATE, DELETE
ON appdb.*
TO 'appuser'@'%';

FLUSH PRIVILEGES;
```

The application user does not receive global administrative privileges.

## Step 4 — Create Application Tables

Run:

```text
sql/02-create-application-tables.sql
```

It creates the `users` table.

## Step 5 — Verify the User

```sql
SHOW DATABASES;

SELECT user, host
FROM mysql.user
WHERE user = 'appuser';

SHOW GRANTS FOR 'appuser'@'%';
```

## Step 6 — Test Application Credentials

Reconnect using:

```text
Username: appuser
Default Schema: appdb
```

Run:

```sql
SELECT DATABASE();
SHOW TABLES;
SELECT COUNT(*) FROM users;
```

## Step 7 — Remove Temporary Public Access

After Workbench setup:

- Set RDS Publicly accessible to No
- Remove your public IP rule from `task11-rds-sg`
- Keep only EC2 Security Group access

## Checklist

- [ ] MySQL Workbench installed
- [ ] Master connection successful
- [ ] `appdb` created
- [ ] `appuser` created
- [ ] Least-privilege grants applied
- [ ] `users` table created
- [ ] Application-user login tested
- [ ] Temporary public access removed
