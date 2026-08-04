# Task 14 — Interview Guide

## 1. Explain the three tiers.

The presentation tier is the ALB, the application tier is private EC2, and the data tier is private RDS.

## 2. Why is the ALB public?

It is the only web entry point and must receive internet traffic.

## 3. Why are EC2 instances private?

They should only receive application traffic from the ALB and administration from the Bastion or Session Manager.

## 4. Why is RDS private?

The database should only accept connections from the application tier.

## 5. Why use Security Group references?

They enforce tier-to-tier access without managing changing IP addresses.

## 6. Why use two public subnets for ALB?

ALB requires subnets in at least two Availability Zones for resilience.

## 7. Why use multiple app subnets?

It distributes application instances across Availability Zones.

## 8. Why use a DB subnet group?

RDS uses it to select private subnets across Availability Zones.

## 9. Why does private EC2 need NAT?

For outbound package downloads and external API access without inbound exposure.

## 10. Does RDS need NAT?

Usually no for normal application traffic.

## 11. What does the Target Group do?

It registers backend instances and performs health checks.

## 12. Why use `/health`?

It provides a lightweight endpoint for ALB health checks.

## 13. What happens when one EC2 fails?

ALB stops sending traffic to the unhealthy target.

## 14. How do you scale the app tier?

Use a Launch Template and Auto Scaling Group.

## 15. How do you secure DB credentials?

Use Secrets Manager and optionally RDS Proxy.

## 16. Why use Multi-AZ RDS?

It improves availability through automatic failover.

## 17. What is the Bastion role?

It provides controlled administration to private instances.

## 18. What is the recommended alternative?

Systems Manager Session Manager.

## 19. How do you add HTTPS?

Use ACM certificate and ALB HTTPS listener.

## 20. How do you improve production readiness?

Add Auto Scaling, WAF, Multi-AZ RDS, Secrets Manager, RDS Proxy, CloudWatch, Flow Logs and IaC.
