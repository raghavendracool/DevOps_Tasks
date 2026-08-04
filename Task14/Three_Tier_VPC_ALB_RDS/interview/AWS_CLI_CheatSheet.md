# Task 14 — AWS CLI Cheat Sheet

## Describe ALB

```bash
aws elbv2 describe-load-balancers \
  --names task14-alb
```

## Target Health

```bash
aws elbv2 describe-target-health \
  --target-group-arn <TARGET_GROUP_ARN>
```

## Describe Private EC2

```bash
aws ec2 describe-instances \
  --filters Name=tag:Name,Values=task14-app-01,task14-app-02,task14-app-03
```

## Describe RDS

```bash
aws rds describe-db-instances \
  --db-instance-identifier task14-mysql-db
```

## ProxyJump

```bash
ssh \
  -i task14-key.pem \
  -J ubuntu@<BASTION_PUBLIC_IP> \
  ubuntu@<APP_PRIVATE_IP>
```

## Check RDS Port

```bash
nc -vz <RDS_ENDPOINT> 3306
```
