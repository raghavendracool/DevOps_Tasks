# Part 4 — EC2, Gunicorn and NGINX Deployment

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Step 1 — Launch Ubuntu EC2

```text
AMI: Ubuntu Server 24.04 LTS
Instance type: t3.micro
Storage: 10 GiB gp3
IAM role: task8-cloud-drive-ec2-role
```

Security Group:

| Port | Source |
|---|---|
| 22 | Your IP |
| 80 | `0.0.0.0/0` |
| 443 | `0.0.0.0/0` when configured |

## Step 2 — Install Packages

```bash
sudo apt update -y
sudo apt install python3-pip python3-venv nginx git -y
```

## Step 3 — Deploy Application

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>/app

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 4 — Configure Environment File

```bash
sudo nano /etc/task8-cloud-drive.env
```

Add:

```text
S3_BUCKET_NAME=<BUCKET_NAME>
AWS_REGION=ap-south-1
FLASK_SECRET_KEY=<LONG_RANDOM_VALUE>
```

Secure:

```bash
sudo chmod 600 /etc/task8-cloud-drive.env
```

## Step 5 — Create systemd Service

Use:

```text
scripts/task8-cloud-drive.service
```

Update the working directory and user path.

Then:

```bash
sudo cp scripts/task8-cloud-drive.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable task8-cloud-drive
sudo systemctl start task8-cloud-drive
```

## Step 6 — Configure NGINX

Use:

```text
scripts/nginx-task8.conf
```

Then:

```bash
sudo cp scripts/nginx-task8.conf \
  /etc/nginx/sites-available/task8-cloud-drive

sudo ln -s \
  /etc/nginx/sites-available/task8-cloud-drive \
  /etc/nginx/sites-enabled/task8-cloud-drive

sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

## Step 7 — Test

Open:

```text
http://<EC2_PUBLIC_IP>
```

## Optional HTTPS

Use:

- Route 53
- Elastic IP
- Let's Encrypt
- Or ALB with ACM certificate

## Checklist

- [ ] EC2 running
- [ ] IAM role attached
- [ ] Gunicorn service active
- [ ] NGINX active
- [ ] Public IP opens application
- [ ] S3 upload and download verified
