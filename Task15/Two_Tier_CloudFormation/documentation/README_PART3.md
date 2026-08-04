# Part 3 — Deploying and Validating the Stack

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Step 1 — Extract the ZIP

```bash
unzip Task15_Two_Tier_CloudFormation.zip
cd Task15_Two_Tier_CloudFormation
```

## Step 2 — Check AWS Identity

```bash
aws sts get-caller-identity
aws configure get region
```

## Step 3 — Confirm Key Pair

```bash
aws ec2 describe-key-pairs \
  --key-names <EC2_KEY_PAIR>
```

## Step 4 — Validate Template

```bash
aws cloudformation validate-template \
  --template-body file://cloudformation/template.yaml
```

Run the supplied script:

```bash
chmod +x scripts/*.sh
./scripts/validate-template.sh
```

For deeper validation, install and run:

```bash
cfn-lint cloudformation/template.yaml
```

## Step 5 — Deploy Stack

```bash
./scripts/deploy-stack.sh \
  task15-two-tier-web \
  <EC2_KEY_PAIR> \
  <YOUR_PUBLIC_IP>/32
```

Equivalent command:

```bash
aws cloudformation deploy \
  --template-file cloudformation/template.yaml \
  --stack-name task15-two-tier-web \
  --parameter-overrides \
    KeyName=<EC2_KEY_PAIR> \
    AdminCidr=<YOUR_PUBLIC_IP>/32 \
  --capabilities CAPABILITY_NAMED_IAM \
  --tags \
    Project=DevOps-Task-15 \
    Environment=Training
```

## Step 6 — Monitor Stack Events

```bash
aws cloudformation describe-stack-events \
  --stack-name task15-two-tier-web \
  --max-items 20
```

Wait:

```bash
aws cloudformation wait stack-create-complete \
  --stack-name task15-two-tier-web
```

Expected stack status:

```text
CREATE_COMPLETE
```


## Verify the ALB Subnet Configuration

After deployment:

```bash
ALB_ARN=$(aws elbv2 describe-load-balancers   --names task15-web-alb   --query 'LoadBalancers[0].LoadBalancerArn'   --output text)

aws elbv2 describe-load-balancers   --load-balancer-arns "$ALB_ARN"   --query 'LoadBalancers[0].AvailabilityZones[].[ZoneName,SubnetId]'   --output table
```

Expected result:

```text
Two different Availability Zones
Two different public subnet IDs
```


## Step 7 — Display Outputs

```bash
aws cloudformation describe-stacks \
  --stack-name task15-two-tier-web \
  --query 'Stacks[0].Outputs' \
  --output table
```

## Step 8 — Review Created Resources

```bash
aws cloudformation list-stack-resources \
  --stack-name task15-two-tier-web \
  --output table
```

## Common Deployment Failures

### Key Pair Does Not Exist

```text
InvalidKeyPair.NotFound
```

Use a key pair from the same Region.

### Insufficient IAM Capability

Add:

```text
--capabilities CAPABILITY_NAMED_IAM
```

### NAT Gateway Elastic IP Limit

Release unused Elastic IPs or request a quota increase.

### Subnet CIDR Conflict

Change the stack CIDR parameters.

### Unsupported Instance Type

Override the instance-type parameters.

## Checklist

- [ ] Template validation passed
- [ ] Stack deployment started
- [ ] Stack reached `CREATE_COMPLETE`
- [ ] All outputs displayed
- [ ] No rollback occurred
