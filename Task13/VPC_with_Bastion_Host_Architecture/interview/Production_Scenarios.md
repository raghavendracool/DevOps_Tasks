# Task 13 — Real-Time Production Scenarios

## Scenario 1 — SSH to Bastion Times Out

Check:

- Bastion public IP
- Bastion Security Group
- Public route table
- Internet Gateway
- NACL
- Local firewall and corporate network

## Scenario 2 — Bastion Is Reachable but Private EC2 Is Not

Check:

- Private EC2 Security Group source
- Private IP
- SSH service
- Local VPC route
- NACL
- Correct key and user

## Scenario 3 — `Permission denied (publickey)`

Check:

- Correct key pair
- File permissions
- Username `ubuntu`
- Authorized keys
- Key copied to the correct instance

## Scenario 4 — Private EC2 Cannot Run `apt update`

Check:

- NAT Gateway state
- Private route table
- NAT public-subnet route
- Internet Gateway
- DNS resolution

## Scenario 5 — NAT Gateway Cost Is Too High

Use VPC endpoints, Session Manager, a controlled NAT instance for small labs, or remove outbound internet when unnecessary.

## Scenario 6 — Bastion Host Is Compromised

Isolate the instance, revoke keys, rotate credentials, inspect logs, replace the Bastion from a clean image and investigate downstream access.

## Scenario 7 — Security Team Rejects Static SSH Keys

Use Session Manager, EC2 Instance Connect Endpoint or short-lived certificates.

## Scenario 8 — Administrator IP Changes Frequently

Use corporate VPN, Client VPN, approved CIDR ranges, Session Manager or identity-aware access.

## Scenario 9 — Multiple Private Subnets Need Access

Use Security Group references and route reachability; avoid one Bastion per subnet unless isolation requires it.

## Scenario 10 — Bastion Needs High Availability

Deploy instances in multiple public subnets across AZs and use automated replacement.

## Scenario 11 — File Transfer Through Bastion Fails

Use `scp -o ProxyJump`, confirm write permissions and test port 22 from Bastion to private EC2.

## Scenario 12 — Private EC2 Accidentally Gets a Public IP

Remove the public IP, disable auto-assign public IP on the subnet and review launch templates.

## Scenario 13 — SSH Works but DNS Does Not

Enable VPC DNS support and hostnames and check DHCP option sets.

## Scenario 14 — Custom NACL Breaks SSH

Allow port 22 and ephemeral return traffic in both directions.

## Scenario 15 — Bastion Disk Is Full

Review logs, package cache and monitoring; rotate logs and rebuild from a clean image if necessary.

## Scenario 16 — Need to Audit Every Command

Use Session Manager session logging or configure shell auditing and centralized log shipping.

## Scenario 17 — Private Instance Needs S3 Only

Use an S3 Gateway Endpoint instead of NAT Gateway.

## Scenario 18 — Private Instance Needs Systems Manager Only

Use SSM, SSMMessages and EC2Messages interface endpoints.

## Scenario 19 — Key Was Copied to Bastion by Mistake

Delete securely, rotate the key pair strategy and verify no unauthorized access occurred.

## Scenario 20 — Direct SSH to Private IP Works from the Internet

This indicates routing or addressing is not as expected. Verify whether the instance has a public IP, VPN path, peering path or exposed network appliance.
