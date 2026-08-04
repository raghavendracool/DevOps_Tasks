# Part 7 — 20 Interview Questions and Answers

[← Part 6](README_PART6.md) | [Main README](../README.md)

## 1. What is an EC2 Launch Template?

A Launch Template is a reusable EC2 configuration containing values such as AMI, instance type, key pair, Security Groups, storage, metadata settings and User Data. Auto Scaling Groups use it to launch consistent instances.

## 2. Why use User Data?

User Data automates bootstrapping when an instance first launches. In this project it installs Apache, Git and `stress-ng`, clones the website and creates instance-specific metadata files.

## 3. Why is Ubuntu used in this project?

Ubuntu is a widely used Linux distribution with predictable `apt` package management. The User Data script uses Ubuntu commands such as `apt-get` and the `apache2` service name.

## 4. What is an Application Load Balancer?

An ALB is a Layer 7 load balancer for HTTP and HTTPS. It distributes requests among healthy targets and supports host-based and path-based routing.

## 5. What is a Target Group?

A Target Group is a collection of backend targets, such as EC2 instances. It defines the protocol, port, health check and routing destination used by the ALB.

## 6. How does the ALB know whether an instance is healthy?

The ALB sends periodic health-check requests to the configured path and port. A target becomes healthy after the required consecutive successful responses.

## 7. Why should the EC2 Security Group allow HTTP from the ALB Security Group?

This ensures users access the application through the load balancer rather than directly reaching EC2 instances. It reduces the exposed attack surface.

## 8. What is an Auto Scaling Group?

An ASG maintains a required number of EC2 instances. It launches replacements for unhealthy instances and adjusts capacity according to scaling policies.

## 9. What is the difference between minimum, desired and maximum capacity?

- Minimum is the lowest number of instances the ASG maintains.
- Desired is the current requested number of instances.
- Maximum is the upper limit the ASG may reach.

## 10. What is Target Tracking scaling?

Target Tracking automatically adjusts capacity to keep a selected metric near a target value. Here, the target is average CPU utilization of 70%.

## 11. What causes scale-out in this project?

Sustained average ASG CPU utilization above the 70% target causes the ASG to increase desired capacity, subject to maximum capacity and warmup rules.

## 12. Why does scale-in not happen immediately?

AWS uses metric evaluation, stabilization and instance warmup behavior to avoid rapid scaling changes. Scale-in is conservative to protect availability.

## 13. What is an instance warmup period?

It is the period after launch during which a new instance is allowed to initialize before its metrics fully influence scaling decisions.

## 14. What is a health check grace period?

It gives a newly launched instance time to boot and initialize before the ASG treats failed load balancer health checks as an instance failure.

## 15. How is high availability achieved?

The ALB spans multiple Availability Zones, the ASG can place instances in multiple subnets, unhealthy targets are removed from traffic and failed instances are replaced.

## 16. How can you prove traffic is reaching different instances?

Display the EC2 Instance ID, Availability Zone and private IP on the page. Repeated ALB requests should show different values when multiple targets are healthy.

## 17. Why use IMDSv2?

IMDSv2 uses session-oriented tokens and provides stronger protection against several metadata access risks compared with unrestricted IMDSv1 access.

## 18. What is S3 Static Website Hosting?

It allows an S3 bucket to serve static HTML, CSS, JavaScript and images through a website endpoint. It cannot execute server-side code.

## 19. Why is a public S3 bucket not the preferred production design?

A better design uses CloudFront with Origin Access Control in front of a private bucket. This provides HTTPS, CDN caching and reduced direct bucket exposure.

## 20. How would you improve this architecture for production?

I would use private EC2 subnets, NAT or VPC endpoints, HTTPS with ACM, Route 53, AWS WAF, CloudFront where appropriate, IAM roles, centralized logs, CloudWatch alarms, Systems Manager instead of public SSH, immutable deployments, infrastructure as code, backups and multi-AZ data services.

## Additional Scenario Questions

### The ALB returns 503. What do you check first?

Check whether the Target Group has healthy targets. Then validate Apache, port 80 rules, health-check path, User Data and subnet routing.

### CPU is 95%, but no new instance launches. Why?

Possible causes include maximum capacity already reached, policy attached to another ASG, instance warmup, missing CloudWatch data, suspended scaling processes, launch failures or account quotas.

### The new instance launches but stays unhealthy. What do you inspect?

Inspect `/var/log/cloud-init-output.log`, Apache status, local HTTP response, Security Groups, health-check path and GitHub connectivity.

### How do you deploy a new application version?

Create a new Launch Template version with updated User Data or an immutable AMI, update the ASG and perform an Instance Refresh with health checks and rollback controls.

## Interview Summary

This project demonstrates practical knowledge of:

- EC2 automation
- Linux and Apache
- ALB and Target Groups
- Health checks
- Auto Scaling
- CloudWatch metrics
- S3 static hosting
- High availability
- Scalability
- Troubleshooting and cleanup
