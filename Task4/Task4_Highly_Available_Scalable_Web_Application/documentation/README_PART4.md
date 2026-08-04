# Part 4 — Auto Scaling Group, Scaling Policy and Stress Testing

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Step 1 — Create the Auto Scaling Group

Open:

```text
EC2 Console → Auto Scaling → Auto Scaling Groups → Create Auto Scaling group
```

Configure:

```text
Name: project-04-web-asg
Launch Template: project-04-web-lt
Version: Default or latest tested version
```

## Step 2 — Select Network Placement

Choose the project VPC.

Select at least two subnets in different Availability Zones:

```text
Public Subnet A
Public Subnet B
```

For production, application instances should normally use private subnets.

## Step 3 — Attach the Load Balancer

Select:

```text
Attach to an existing load balancer
Choose from your load balancer target groups
Target Group: project-04-web-tg
```

Enable:

```text
Elastic Load Balancing health checks
```

Recommended health check grace period:

```text
300 seconds
```

This gives Ubuntu, Git, Apache and website deployment time to complete.

## Step 4 — Configure Capacity

Set:

| Capacity | Value |
|---|---:|
| Desired | 1 |
| Minimum | 1 |
| Maximum | 3 |

Create the ASG.

## Step 5 — Wait for the First Healthy Instance

Open:

```text
Auto Scaling Group → Instance management
```

Expected:

```text
Lifecycle: InService
Health status: Healthy
```

Then check:

```text
Target Group → Targets
```

Expected:

```text
Health status: Healthy
```

## Step 6 — Test the Website Through the ALB

Open:

```text
http://<ALB_DNS_NAME>
```

Refresh the page.

At desired capacity `1`, the same instance normally serves each request.

## Step 7 — Configure Target Tracking Scaling

Open:

```text
Auto Scaling Group → Automatic scaling → Create dynamic scaling policy
```

Configure:

```text
Policy type: Target tracking scaling
Policy name: project-04-cpu-70-policy
Metric type: Average CPU utilization
Target value: 70
Instance warmup: 300 seconds
Disable scale in: Unchecked
```

Save the policy.

AWS automatically creates CloudWatch alarms for scale-out and scale-in control.

## Step 8 — Generate CPU Load

SSH to the running instance:

```bash
ssh -i project-key.pem ubuntu@<PUBLIC_IP>
```

The User Data installs `stress-ng`. Confirm:

```bash
stress-ng --version
nproc
```

Run the supplied script:

```bash
chmod +x cpu-stress-test.sh
./cpu-stress-test.sh
```

Or run directly:

```bash
stress-ng --cpu "$(nproc)" --cpu-load 100 --timeout 15m --metrics-brief
```

Monitor CPU:

```bash
top
```

## Step 9 — Verify Scale-Out

Check CloudWatch:

```text
EC2 → Monitoring → CPUUtilization
```

Check ASG:

```text
Auto Scaling Group → Activity
```

Expected sequence:

```text
Average CPU rises above target
→ Scaling activity starts
→ New EC2 instance launches
→ User Data runs
→ Target becomes healthy
→ Desired capacity increases
```

The ASG may launch one or more instances, but cannot exceed maximum capacity `3`.

## Step 10 — Verify Load Distribution

Once at least two targets are healthy, refresh the ALB URL repeatedly.

The displayed values should change:

```text
Instance ID
Availability Zone
Private IP
Hostname
```

CLI test:

```bash
for i in {1..10}; do
  curl -s http://<ALB_DNS_NAME>/server-info.js
  echo
  sleep 1
done
```

> ALB routing is not guaranteed to alternate exactly on every refresh.

## Step 11 — Verify Scale-In

After `stress-ng` finishes, allow CPU utilization to fall.

Check:

```text
CloudWatch CPUUtilization
Auto Scaling Group → Activity
EC2 Instances
Target Group → Targets
```

Expected:

```text
CPU returns below target
→ Stabilization and cooldown period passes
→ ASG terminates extra instances
→ Capacity returns toward desired/minimum capacity
```

Scale-in is intentionally slower to prevent rapid capacity changes.

## Step 12 — Optional Faster Demonstration

For a lab only, you can temporarily:

- Lower target CPU to `30%`
- Use a longer stress period
- Reduce instance warmup after validating boot time

Return the final policy to:

```text
Target CPU: 70%
```

## Troubleshooting Scaling

### CPU Is High but No Scale-Out

Check:

- Policy attached to the correct ASG
- Maximum capacity is greater than desired capacity
- CloudWatch metric is available
- Instance warmup has completed
- ASG activities do not show launch failures

### New Instance Launch Fails

Check:

- AMI is valid in the selected region
- Instance type capacity is available
- Launch Template has a valid Security Group
- Key pair exists
- Service quota is not exceeded
- Subnet has available IP addresses

### New Target Remains Unhealthy

Inspect:

```bash
sudo tail -200 /var/log/cloud-init-output.log
sudo systemctl status apache2 --no-pager
curl -I http://localhost
```

### Scale-In Does Not Occur Immediately

Normal reasons include:

- Target tracking stabilization
- Instance warmup
- CPU metric evaluation periods
- Minimum capacity restriction
- Instance scale-in protection

## Part 4 Checklist

- [ ] ASG created from Launch Template
- [ ] Two subnets selected
- [ ] Target Group attached
- [ ] ELB health checks enabled
- [ ] Grace period configured
- [ ] Min 1, desired 1, max 3
- [ ] Initial target healthy
- [ ] Target Tracking policy created
- [ ] CPU target set to 70%
- [ ] `stress-ng` executed
- [ ] Scale-out observed
- [ ] Multiple targets healthy
- [ ] Traffic distribution verified
- [ ] Scale-in observed

[Next: Part 5 — Amazon S3 Static Website Hosting →](README_PART5.md)
