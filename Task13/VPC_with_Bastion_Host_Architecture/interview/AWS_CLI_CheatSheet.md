# Task 13 — AWS CLI Cheat Sheet

## Describe VPC

```bash
aws ec2 describe-vpcs \
  --filters Name=tag:Name,Values=task13-vpc
```

## Describe Subnets

```bash
aws ec2 describe-subnets \
  --filters Name=vpc-id,Values=<VPC_ID>
```

## Describe Route Tables

```bash
aws ec2 describe-route-tables \
  --filters Name=vpc-id,Values=<VPC_ID>
```

## Describe Instances

```bash
aws ec2 describe-instances \
  --filters Name=tag:Name,Values=task13-bastion-host,task13-private-ec2 \
  --query 'Reservations[].Instances[].[Tags[?Key==`Name`].Value|[0],InstanceId,PrivateIpAddress,PublicIpAddress,SubnetId]'
```

## ProxyJump SSH

```bash
ssh \
  -i task13-key.pem \
  -J ubuntu@<BASTION_PUBLIC_IP> \
  ubuntu@<PRIVATE_EC2_IP>
```

## ProxyJump SCP

```bash
scp \
  -i task13-key.pem \
  -o ProxyJump=ubuntu@<BASTION_PUBLIC_IP> \
  test.txt \
  ubuntu@<PRIVATE_EC2_IP>:/home/ubuntu/
```

## Check NAT Gateway

```bash
aws ec2 describe-nat-gateways \
  --filter Name=vpc-id,Values=<VPC_ID>
```
