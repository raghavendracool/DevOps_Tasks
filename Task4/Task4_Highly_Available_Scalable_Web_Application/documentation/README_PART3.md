# Part 3 — Target Group and Application Load Balancer

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Step 1 — Create the Target Group

Open:

```text
EC2 Console → Load Balancing → Target Groups → Create target group
```

Configure:

```text
Target type: Instances
Target group name: project-04-web-tg
Protocol: HTTP
Port: 80
IP address type: IPv4
VPC: Project VPC
Protocol version: HTTP1
```

Do not manually register temporary instances when the ASG will manage registration.

## Step 2 — Configure the Health Check

Recommended settings:

| Setting | Value |
|---|---|
| Protocol | HTTP |
| Path | `/` |
| Port | Traffic port |
| Healthy threshold | 2 |
| Unhealthy threshold | 2 |
| Timeout | 5 seconds |
| Interval | 30 seconds |
| Success codes | `200` |

Create the Target Group.

## Step 3 — Create the Application Load Balancer

Open:

```text
EC2 Console → Load Balancers → Create Load Balancer
```

Choose:

```text
Application Load Balancer
```

Configure:

```text
Name: project-04-alb
Scheme: Internet-facing
IP address type: IPv4
VPC: Project VPC
```

Select at least two Availability Zones and one public subnet from each.

Example:

```text
ap-south-1a → Public Subnet A
ap-south-1b → Public Subnet B
```

## Step 4 — Attach the ALB Security Group

Select:

```text
project-04-alb-sg
```

Remove any unnecessary default Security Group.

## Step 5 — Configure the Listener

Create:

```text
Protocol: HTTP
Port: 80
Default action: Forward to project-04-web-tg
```

Create the Load Balancer.

Wait until its state becomes:

```text
Active
```

## Step 6 — Record the ALB DNS Name

Open the ALB details and copy:

```text
DNS name: project-04-alb-xxxxxxxx.ap-south-1.elb.amazonaws.com
```

You will test this after the ASG launches healthy instances.

## Step 7 — Understand Target Registration

When the ASG is attached to the Target Group:

1. ASG launches an instance.
2. EC2 completes User Data.
3. Apache begins listening on port 80.
4. ASG registers the instance in the Target Group.
5. ALB performs health checks.
6. Target becomes `Healthy`.
7. ALB begins forwarding requests.

## Step 8 — Validate the ALB Configuration

Check:

```text
ALB State: Active
Listener: HTTP:80
Default Action: project-04-web-tg
Subnets: At least two AZs
Security Group: project-04-alb-sg
```

Check Target Group:

```text
Protocol: HTTP:80
Health check path: /
Expected success code: 200
```

## Step 9 — Optional HTTPS Improvement

For production:

1. Request or import a certificate in AWS Certificate Manager.
2. Create an HTTPS listener on port 443.
3. Attach the certificate.
4. Redirect HTTP port 80 to HTTPS port 443.
5. Create a DNS record pointing your domain to the ALB.

## Common ALB Problems

### ALB Returns `503 Service Unavailable`

Usually no healthy targets are available.

Check:

```text
Target Group → Targets → Health status
```

Then verify:

```bash
sudo systemctl status apache2
sudo ss -lntp | grep ':80'
curl -I http://localhost
```

### Target Shows `Unhealthy`

Check:

- Target Group VPC matches EC2 VPC
- EC2 Security Group permits port 80 from ALB Security Group
- Apache is running
- Health check path returns HTTP 200
- User Data completed
- Network ACLs permit traffic

### ALB DNS Does Not Open

Check:

- ALB is internet-facing
- ALB subnets are public
- Route table contains Internet Gateway route
- ALB Security Group permits port 80
- Targets are healthy

## Part 3 Checklist

- [ ] Target Group created
- [ ] HTTP port 80 configured
- [ ] Health check path `/`
- [ ] ALB created
- [ ] Internet-facing scheme selected
- [ ] Two Availability Zones selected
- [ ] Public subnets selected
- [ ] ALB Security Group attached
- [ ] Listener forwards to Target Group
- [ ] ALB state is Active
- [ ] DNS name recorded

[Next: Part 4 — Auto Scaling, Policy and Stress Testing →](README_PART4.md)
