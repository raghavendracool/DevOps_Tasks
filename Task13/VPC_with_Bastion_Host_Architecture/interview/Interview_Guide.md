# Task 13 — Interview Guide

## 1. What is a Bastion Host?

A Bastion Host is a hardened entry server used to access resources in private networks.

## 2. Why is the Bastion Host in a public subnet?

It needs a route to the Internet Gateway and a public address so approved administrators can reach it.

## 3. Why is the application instance in a private subnet?

It reduces direct internet exposure and allows access only through controlled paths.

## 4. What is the difference between a public and private subnet?

A public subnet has a default route to an Internet Gateway. A private subnet does not.

## 5. Does a public subnet automatically make an EC2 instance public?

No. The instance also needs a public IP and Security Group access.

## 6. How does the private instance reach the internet?

Through a NAT Gateway or NAT instance in a public subnet.

## 7. Can the internet initiate a connection through a NAT Gateway?

No. NAT Gateway supports outbound connections and return traffic, not unsolicited inbound traffic.

## 8. Why reference the Bastion Security Group in the private Security Group?

It restricts SSH to instances associated with the Bastion Security Group instead of using IP addresses.

## 9. What is ProxyJump?

An SSH feature that routes the connection through an intermediate SSH server.

## 10. Why is copying the private key to the Bastion risky?

If the Bastion is compromised, the private key can be stolen and used to access downstream systems.

## 11. What is SSH agent forwarding?

It allows authentication through a remote host while keeping the private key on the local machine.

## 12. What is the risk of agent forwarding?

A compromised Bastion may misuse the forwarded agent during the session.

## 13. What is the difference between Security Groups and NACLs?

Security Groups are stateful and instance-level. NACLs are stateless and subnet-level.

## 14. Why does the public route table need an Internet Gateway route?

It enables internet traffic for public-subnet resources with public IP addresses.

## 15. Why must NAT Gateway be in a public subnet?

It needs a public route to the Internet Gateway and an Elastic IP.

## 16. How do you make Bastion highly available?

Deploy Bastion instances across multiple Availability Zones, use Auto Scaling, and provide controlled access through stable endpoints where needed.

## 17. How do you monitor Bastion access?

Use authentication logs, CloudWatch Agent, VPC Flow Logs, CloudTrail, GuardDuty and centralized SIEM logging.

## 18. What is the modern alternative?

AWS Systems Manager Session Manager.

## 19. What are the benefits of Session Manager?

No public IP, no inbound SSH, IAM authorization, audit logs and session recording.

## 20. How would you improve this design for production?

Use multiple AZs, Session Manager, private endpoints, strong identity controls, hardened images, centralized logging and no static private keys on the Bastion.
