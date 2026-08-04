# Part 4 — ALB, Bastion and Application Verification

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Step 1 — Confirm the ALB Spans Two Availability Zones

```bash
aws elbv2 describe-load-balancers   --names task15-web-alb   --query 'LoadBalancers[0].AvailabilityZones[].[ZoneName,SubnetId]'   --output table
```

Confirm that two public subnet IDs and two Availability Zones are displayed.

## Step 2 — Open the Application

Get URL:

```bash
aws cloudformation describe-stacks \
  --stack-name task15-two-tier-web \
  --query "Stacks[0].Outputs[?OutputKey=='ApplicationURL'].OutputValue" \
  --output text
```

Open the result in a browser.

Expected page:

```text
Task 15 — Two-Tier Web Application
Deployed using AWS CloudFormation
Instance ID
Availability Zone
Private IP
```

## Step 3 — Test with curl

```bash
curl -I http://<ALB_DNS_NAME>
curl http://<ALB_DNS_NAME>
```

Expected:

```text
HTTP/1.1 200 OK
```

## Step 4 — Check Target Health

Get Target Group ARN:

```bash
TARGET_GROUP_ARN=$(aws cloudformation describe-stacks \
  --stack-name task15-two-tier-web \
  --query "Stacks[0].Outputs[?OutputKey=='TargetGroupArn'].OutputValue" \
  --output text)
```

Check:

```bash
aws elbv2 describe-target-health \
  --target-group-arn "$TARGET_GROUP_ARN"
```

Expected:

```text
State: healthy
```

## Step 5 — Connect to Bastion

```bash
ssh \
  -i <KEY_FILE>.pem \
  ubuntu@<BASTION_PUBLIC_IP>
```

## Step 6 — Connect to Web Server Using ProxyJump

Recommended from your local machine:

```bash
ssh \
  -i <KEY_FILE>.pem \
  -J ubuntu@<BASTION_PUBLIC_IP> \
  ubuntu@<WEB_SERVER_PRIVATE_IP>
```

## Step 7 — Verify NGINX

On Web Server:

```bash
sudo systemctl status nginx --no-pager
sudo nginx -t
curl -I http://localhost
cat /var/www/html/index.html
```

## Step 8 — Verify Network Placement

Bastion:

```text
Public subnet
Public IP present
```

Web Server:

```text
Private subnet
No public IP
```

## Step 9 — Verify NAT Egress

On Web Server:

```bash
curl -I https://aws.amazon.com
curl -s https://checkip.amazonaws.com
```

The egress IP should be the NAT Gateway Elastic IP.

## Step 10 — Confirm Only ALB Serves the Website

The Web Server Security Group permits port 80 only from the ALB Security Group.

Direct browser access to the Web Server is impossible because it has no public IP.

## Verification Checklist

- [ ] ALB DNS opens
- [ ] HTTP 200 returned
- [ ] Target is healthy
- [ ] Bastion SSH works
- [ ] ProxyJump to Web Server works
- [ ] NGINX is active
- [ ] Web Server has no public IP
- [ ] NAT outbound internet works
