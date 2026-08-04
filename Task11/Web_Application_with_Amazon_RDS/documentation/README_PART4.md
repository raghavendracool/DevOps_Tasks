# Part 4 — Flask Application and EC2 Deployment

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Application Features

- Register a new user
- Hash the password
- Store the user in RDS MySQL
- Log in using RDS data
- Verify successful database connectivity
- Display a dashboard after login

## Application Structure

```text
app/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
└── static/
    └── style.css
```

## Step 1 — Launch Ubuntu EC2

Configure:

```text
AMI: Ubuntu Server 24.04 LTS
Instance type: t3.micro
Security Group: task11-web-sg
IAM role: Optional Secrets Manager role
```

Inbound:

| Type | Port | Source |
|---|---:|---|
| SSH | 22 | Your public IP |
| HTTP | 80 | `0.0.0.0/0` |
| HTTPS | 443 | `0.0.0.0/0` when configured |

## Step 2 — Install Packages

```bash
sudo apt update -y
sudo apt install python3-pip python3-venv nginx git mysql-client -y
```

## Step 3 — Deploy Application

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>/app

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 4 — Configure Database Credentials

Create:

```bash
sudo nano /etc/task11-rds-app.env
```

Add:

```text
DB_HOST=<RDS_ENDPOINT>
DB_PORT=3306
DB_NAME=appdb
DB_USER=appuser
DB_PASSWORD=<APPLICATION_DB_PASSWORD>
FLASK_SECRET_KEY=<LONG_RANDOM_VALUE>
DB_SSL_CA=/etc/ssl/certs/global-bundle.pem
```

Secure:

```bash
sudo chmod 600 /etc/task11-rds-app.env
```

The package also documents Secrets Manager as the recommended production approach.

## Step 5 — Download the RDS CA Bundle

```bash
sudo curl -o /etc/ssl/certs/global-bundle.pem \
  https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

sudo chmod 644 /etc/ssl/certs/global-bundle.pem
```

## Step 6 — Test Database Connectivity

```bash
set -a
source /etc/task11-rds-app.env
set +a

python scripts/test_db_connection.py
```

## Step 7 — Configure Gunicorn

Use:

```text
scripts/task11-rds-app.service
```

Update paths when necessary.

```bash
sudo cp scripts/task11-rds-app.service \
  /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable task11-rds-app
sudo systemctl start task11-rds-app
```

## Step 8 — Configure NGINX

Use:

```text
scripts/nginx-task11.conf
```

```bash
sudo cp scripts/nginx-task11.conf \
  /etc/nginx/sites-available/task11-rds-app

sudo ln -s \
  /etc/nginx/sites-available/task11-rds-app \
  /etc/nginx/sites-enabled/task11-rds-app

sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

## Step 9 — Verify Login

Open:

```text
http://<EC2_PUBLIC_IP>
```

1. Register a new user.
2. Log out.
3. Log in using the created credentials.
4. Confirm the dashboard loads.
5. Verify the row in MySQL Workbench.

## Checklist

- [ ] EC2 launched
- [ ] Dependencies installed
- [ ] Application deployed
- [ ] Environment file secured
- [ ] TLS CA bundle installed
- [ ] DB connectivity test passed
- [ ] Gunicorn running
- [ ] NGINX running
- [ ] Registration and login verified
