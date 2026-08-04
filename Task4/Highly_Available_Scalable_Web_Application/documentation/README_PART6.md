# Part 6 — Verification, Cleanup and Troubleshooting

[← Part 5](README_PART5.md) | [Next: Part 7 →](README_PART7.md)

## End-to-End Verification

### 1. Launch Template

Verify:

- Ubuntu AMI
- Correct instance type
- EC2 Security Group
- Key pair
- IMDSv2 required
- User Data present
- Root volume delete-on-termination enabled

### 2. Auto Scaling Group

Verify:

```text
Minimum: 1
Desired: 1
Maximum: 3
Subnets: At least two Availability Zones
Target Group: project-04-web-tg
Health check type: ELB
```

### 3. Target Group

Expected:

```text
At least one target: Healthy
Protocol: HTTP
Port: 80
Health check path: /
```

### 4. Application Load Balancer

Open:

```text
http://<ALB_DNS_NAME>
```

Expected:

- Website loads
- HTTP response is 200
- Server information is visible
- Repeated requests are successful

CLI:

```bash
curl -I http://<ALB_DNS_NAME>
curl -s http://<ALB_DNS_NAME>/server-info.js
```

### 5. High Availability

With two healthy targets:

1. Note both Instance IDs.
2. Terminate one instance from the EC2 console.
3. Confirm the website remains available.
4. Confirm ASG launches a replacement.
5. Confirm the replacement becomes healthy.

Do this only in the training environment.

### 6. Scalability

Run `stress-ng` and verify:

- CPU crosses target
- Scaling activity is recorded
- Desired capacity rises
- New instance becomes healthy
- Traffic reaches multiple instances
- Capacity later decreases

### 7. S3 Website

Verify:

```text
S3 website endpoint opens
index.html loads
CSS and JavaScript load
No 403 or 404 errors
```

## Evidence to Capture

Recommended screenshots:

```text
01-launch-template.png
02-user-data.png
03-target-group.png
04-alb.png
05-asg-capacity.png
06-scaling-policy.png
07-healthy-targets.png
08-alb-website-instance-a.png
09-alb-website-instance-b.png
10-cloudwatch-cpu.png
11-scale-out-activity.png
12-scale-in-activity.png
13-s3-hosting.png
14-s3-website.png
```

## Troubleshooting Matrix

| Problem | Likely Cause | Check |
|---|---|---|
| ALB 503 | No healthy target | Target health |
| Target unhealthy | SG, Apache or path issue | Port 80 and `/` |
| User Data failed | Repo or internet issue | cloud-init log |
| No scale-out | Policy or max capacity | ASG policy/activity |
| EC2 launch failed | AMI, quota or subnet | Activity error |
| S3 403 | Public access/policy | Bucket permissions |
| S3 404 | Incorrect path/case | Object key |
| CSS missing | Wrong relative path | Browser Network tab |

## Useful Ubuntu Commands

```bash
sudo systemctl status apache2 --no-pager
sudo systemctl restart apache2
sudo apache2ctl configtest
sudo ss -lntp
curl -I http://localhost
sudo tail -200 /var/log/cloud-init-output.log
sudo journalctl -u apache2 --no-pager -n 100
df -h
free -m
top
```

## Useful AWS CLI Commands

```bash
aws sts get-caller-identity
aws ec2 describe-instances \
  --filters "Name=tag:aws:autoscaling:groupName,Values=project-04-web-asg"

aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names project-04-web-asg

aws autoscaling describe-scaling-activities \
  --auto-scaling-group-name project-04-web-asg \
  --max-items 20

aws elbv2 describe-target-health \
  --target-group-arn <TARGET_GROUP_ARN>

aws s3 ls s3://<BUCKET_NAME>/ --recursive
```

## Cleanup Order

Delete resources after completing the lab to avoid charges.

### Step 1 — Scale Down and Delete ASG

```text
Auto Scaling Groups → project-04-web-asg
```

Set desired and minimum capacity to `0`, wait for instances to terminate, then delete the ASG.

### Step 2 — Delete the Application Load Balancer

```text
Load Balancers → project-04-alb → Delete
```

### Step 3 — Delete the Target Group

```text
Target Groups → project-04-web-tg → Delete
```

### Step 4 — Delete the Launch Template

```text
Launch Templates → project-04-web-lt → Delete
```

### Step 5 — Delete Remaining EC2 Instances

Confirm no manually launched test instances remain.

### Step 6 — Empty and Delete the S3 Bucket

```bash
aws s3 rm s3://<BUCKET_NAME>/ --recursive
aws s3api delete-bucket --bucket <BUCKET_NAME> --region ap-south-1
```

### Step 7 — Delete Security Groups

Delete:

```text
project-04-web-sg
project-04-alb-sg
```

Delete the EC2 Security Group first if it references the ALB Security Group.

### Step 8 — Review CloudWatch and Billing

Check for:

- Remaining alarms
- Unexpected EC2 instances
- Load Balancers
- NAT Gateways
- Elastic IP addresses
- S3 objects
- Snapshots
- Custom AMIs

## Final Validation Checklist

- [ ] Website opens through ALB
- [ ] Target health is Healthy
- [ ] Instance information is displayed
- [ ] Two-AZ configuration is present
- [ ] Scale-out tested
- [ ] Scale-in tested
- [ ] S3 website opens
- [ ] Screenshots collected
- [ ] All chargeable resources cleaned up
- [ ] GitHub README updated

[Next: Part 7 — Interview Questions and Answers →](README_PART7.md)
