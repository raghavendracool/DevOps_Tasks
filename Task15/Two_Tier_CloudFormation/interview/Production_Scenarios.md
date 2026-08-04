# Task 15 — Real-Time Production Scenarios

## Scenario 1 — Stack Is in `ROLLBACK_COMPLETE`

Review stack events, correct the template or parameters, delete the failed stack and redeploy.

## Scenario 2 — ALB Returns 503

Check Target Group health, NGINX, port 80 rules and User Data logs.

## Scenario 3 — Web Server Creation Times Out

The CreationPolicy did not receive `cfn-signal`. Check NAT connectivity, package installation and cloud-init logs.

## Scenario 4 — NAT Gateway Fails to Create

Check Elastic IP quota, public-subnet route and Internet Gateway attachment.

## Scenario 5 — Key Pair Is Not Found

Key pairs are regional. Use a key from the deployment Region.

## Scenario 6 — ALB Template Uses One Subnet

Deployment fails because an ALB needs at least two Availability Zone subnets.

## Scenario 7 — Security Review Rejects Bastion Host

Use Systems Manager Session Manager or EC2 Instance Connect Endpoint.

## Scenario 8 — Template Update Replaces the EC2 Instance

Review the Change Set and plan for immutable replacement or Auto Scaling.

## Scenario 9 — User Data Change Does Not Re-run

User Data normally runs only during initial launch. Replace the instance, use `cfn-init`, or use Systems Manager.

## Scenario 10 — Someone Manually Changes a Security Group

Run stack drift detection and update through CloudFormation.

## Scenario 11 — Named IAM Role Already Exists

Use a unique generated name, import the resource or change the role name.

## Scenario 12 — Web Server Has No Internet

Check NAT state, private route table and NAT public-subnet routing.

## Scenario 13 — Stack Deletion Is Stuck

Check dependency conflicts, deletion protection and resources modified outside the stack.

## Scenario 14 — Production Requires HTTPS

Add an ACM certificate, HTTPS listener and HTTP redirect.

## Scenario 15 — Production Requires Multiple Web Servers

Replace the fixed EC2 instance with a Launch Template and Auto Scaling Group.

## Scenario 16 — NAT Gateway Cost Is High

Use VPC endpoints, a pre-baked AMI and remove unnecessary internet dependencies.

## Scenario 17 — Need Multiple Environments

Use parameter files, nested stacks, CI/CD and separate accounts.

## Scenario 18 — Template Becomes Too Large

Upload to S3 and split into nested stacks or reusable modules.

## Scenario 19 — A Deployment Must Be Approved

Generate a Change Set and require manual approval before execution.

## Scenario 20 — Multi-Account Deployment Is Required

Use CloudFormation StackSets with Organizations integration.
