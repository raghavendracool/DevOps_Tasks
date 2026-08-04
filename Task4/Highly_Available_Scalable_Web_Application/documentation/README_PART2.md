# Part 2 — Launch Template, User Data, EC2, Apache and GitHub Website

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Prepare the Website Files

The supplied files are available under:

```text
website/
├── index.html
├── style.css
└── script.js
```

Create a public GitHub repository and push these files:

```bash
git init
git branch -M main
git add .
git commit -m "Add highly available AWS web application"
git remote add origin https://github.com/<username>/<repository>.git
git push -u origin main
```

Record the clone URL:

```text
https://github.com/<username>/<repository>.git
```

## Step 2 — Create the ALB Security Group

Open:

```text
EC2 Console → Network & Security → Security Groups → Create security group
```

Configure:

```text
Name: project-04-alb-sg
VPC: Select your project VPC
```

Inbound:

```text
HTTP | TCP | 80 | 0.0.0.0/0
```

Keep the default outbound rule.

## Step 3 — Create the EC2 Security Group

Configure:

```text
Name: project-04-web-sg
VPC: Same VPC as the ALB
```

Inbound:

```text
HTTP | TCP | 80 | Source: project-04-alb-sg
SSH  | TCP | 22 | Source: My IP
```

This permits HTTP only from the ALB while retaining restricted SSH access.

## Step 4 — Review the Ubuntu User Data Script

The complete script is supplied as:

```text
scripts/user-data.sh
```

Before using it, replace:

```bash
REPO_URL="https://github.com/<username>/<repository>.git"
```

The script:

1. Updates Ubuntu packages.
2. Installs Apache, Git, curl and `stress-ng`.
3. Clones the public GitHub repository.
4. Copies website files to `/var/www/html`.
5. Retrieves metadata using IMDSv2.
6. Generates `/var/www/html/server-info.js`.
7. Enables and starts Apache.

Important excerpt:

```bash
TOKEN=$(curl -sS -X PUT \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
  http://169.254.169.254/latest/api/token)

INSTANCE_ID=$(curl -sS \
  -H "X-aws-ec2-metadata-token: ${TOKEN}" \
  http://169.254.169.254/latest/meta-data/instance-id)
```

## Step 5 — Create the Launch Template

Open:

```text
EC2 Console → Instances → Launch Templates → Create launch template
```

Configure:

```text
Launch template name: project-04-web-lt
Template version description: Ubuntu Apache web server v1
```

### AMI

Choose a current Ubuntu Server LTS AMI for your region, such as Ubuntu Server 24.04 LTS.

### Instance Type

For training:

```text
t3.micro
```

Choose a type supported by your account and region.

### Key Pair

Select your existing EC2 key pair.

### Network Settings

Do not select a fixed subnet in the Launch Template. The Auto Scaling Group will select multiple subnets.

Select:

```text
Security Group: project-04-web-sg
```

### Storage

Recommended training setting:

```text
Root volume: 8–10 GiB
Type: gp3
Delete on termination: Enabled
```

### Advanced Details

Set:

```text
Metadata version: V2 only
Metadata response hop limit: 1
```

Paste the contents of `scripts/user-data.sh` into **User data**.

Create the Launch Template.

## Step 6 — Test the Launch Template Manually

Before creating the ASG, test one instance:

```text
Launch Templates → project-04-web-lt → Actions → Launch instance from template
```

Select one public subnet and launch.

Wait until:

```text
Instance state: Running
Status checks: 2/2 passed
```

## Step 7 — Validate Apache

SSH to the instance when required:

```bash
chmod 400 project-key.pem
ssh -i project-key.pem ubuntu@<EC2_PUBLIC_IP>
```

Check services:

```bash
sudo systemctl status apache2 --no-pager
sudo apache2ctl configtest
curl -I http://localhost
```

Expected:

```text
HTTP/1.1 200 OK
Syntax OK
```

Check files:

```bash
ls -la /var/www/html
cat /var/www/html/server-info.js
```

View cloud-init logs:

```bash
sudo tail -100 /var/log/cloud-init-output.log
sudo journalctl -u apache2 --no-pager -n 50
```

## Step 8 — Verify Instance Information

Because the EC2 Security Group allows HTTP only from the ALB, direct browser access may be blocked. For temporary testing, you can:

- Use `curl http://localhost` over SSH, or
- Temporarily allow HTTP from your public IP, test, and remove the rule

The page should display:

- EC2 Instance ID
- Availability Zone
- Private IP
- Hostname
- Current time

## Step 9 — Fix Common User Data Problems

### Git Clone Fails

Check:

```bash
git ls-remote https://github.com/<username>/<repository>.git
```

The repository must be public unless authentication is securely configured.

### Apache Shows Default Page

Check whether files were copied:

```bash
sudo find /var/www/html -maxdepth 2 -type f -print
```

Remove the default file before copying:

```bash
sudo rm -rf /var/www/html/*
```

### Package Installation Fails

Confirm the instance has outbound internet access:

```bash
curl -I https://archive.ubuntu.com
curl -I https://github.com
```

### Metadata Is Empty

Verify IMDSv2:

```bash
TOKEN=$(curl -sS -X PUT \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 60" \
  http://169.254.169.254/latest/api/token)

curl -sS \
  -H "X-aws-ec2-metadata-token: ${TOKEN}" \
  http://169.254.169.254/latest/meta-data/instance-id
```

## Part 2 Checklist

- [ ] Website code pushed to a public GitHub repository
- [ ] ALB Security Group created
- [ ] EC2 Security Group created
- [ ] User Data repository URL updated
- [ ] Launch Template created
- [ ] Ubuntu AMI selected
- [ ] IMDSv2 required
- [ ] Test EC2 launched
- [ ] Apache active
- [ ] Website files deployed
- [ ] Instance metadata displayed
- [ ] Test EC2 terminated before ASG deployment

[Next: Part 3 — Target Group and Application Load Balancer →](README_PART3.md)
