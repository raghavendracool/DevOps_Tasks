# Part 2 — CloudFormation Template Structure

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Main Template

```text
cloudformation/template.yaml
```


## Correct Resource Placement

| Resource | Subnet Placement |
|---|---|
| Application Load Balancer | Public Subnet A and Public Subnet B |
| Bastion Host | Public Subnet A |
| NAT Gateway | Public Subnet A |
| Private Web Server | Private Subnet A |

The ALB must not be configured with only one subnet. Both public subnets must be selected during deployment.


## Template Sections

```yaml
AWSTemplateFormatVersion:
Description:
Metadata:
Parameters:
Mappings:
Conditions:
Resources:
Outputs:
```

The supplied template uses:

- Parameters
- Intrinsic functions
- Explicit dependencies
- Resource references
- Security Group references
- User Data with `Fn::Sub`
- Stack outputs

## Network Resources

```text
AWS::EC2::VPC
AWS::EC2::InternetGateway
AWS::EC2::VPCGatewayAttachment
AWS::EC2::Subnet
AWS::EC2::RouteTable
AWS::EC2::Route
AWS::EC2::SubnetRouteTableAssociation
AWS::EC2::EIP
AWS::EC2::NatGateway
```

## Load Balancing Resources

```text
AWS::ElasticLoadBalancingV2::LoadBalancer
AWS::ElasticLoadBalancingV2::TargetGroup
AWS::ElasticLoadBalancingV2::Listener
```

## Compute Resources

```text
AWS::EC2::Instance
```

The assignment mentions launch configuration. Because this project launches one fixed web server rather than an Auto Scaling Group, a Launch Configuration is unnecessary. The EC2 instance configuration is directly defined in `AWS::EC2::Instance`.

For a scalable production version, use:

```text
AWS::EC2::LaunchTemplate
AWS::AutoScaling::AutoScalingGroup
```

Launch Configurations are a legacy pattern; Launch Templates are preferred for new designs.

## IAM Resources

```text
AWS::IAM::Role
AWS::IAM::InstanceProfile
```

The Web Server role includes:

```text
AmazonSSMManagedInstanceCore
```

This allows later migration from Bastion access to Systems Manager Session Manager.

## User Data

The Web Server User Data:

1. Updates Ubuntu packages.
2. Installs NGINX.
3. Retrieves instance metadata using IMDSv2.
4. Creates a custom HTML page.
5. Enables and starts NGINX.

## Dependency Handling

Important dependencies include:

```text
Public routes depend on the Internet Gateway attachment.
NAT Gateway depends on the public default route.
Web Server depends on the private NAT route.
ALB depends on the Internet Gateway attachment.
Listener depends on ALB and Target Group.
```

## Outputs

The template returns:

```text
ApplicationURL
LoadBalancerDNSName
BastionPublicIP
BastionPrivateIP
WebServerPrivateIP
VPCId
PublicSubnetAId
PublicSubnetBId
PrivateSubnetId
TargetGroupArn
```

## Validation Files

```text
scripts/validate-template.sh
scripts/deploy-stack.sh
scripts/delete-stack.sh
```

## Checklist

- [ ] Parameters reviewed
- [ ] CIDRs do not overlap
- [ ] Existing key-pair name known
- [ ] Security Group references understood
- [ ] User Data reviewed
- [ ] Outputs reviewed
