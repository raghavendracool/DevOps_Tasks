# Task 7 — AWS CLI Cheat Sheet

## Lambda Configuration

```bash
aws lambda get-function-configuration \
  --function-name task7-compliance-monitor
```

## Set 30-Second Timeout

```bash
aws lambda update-function-configuration \
  --function-name task7-compliance-monitor \
  --timeout 30
```

## Invoke Function

```bash
aws lambda invoke \
  --function-name task7-compliance-monitor \
  --payload '{"source":"manual-cli-test"}' \
  response.json
```

## Tail Logs

```bash
aws logs tail \
  /aws/lambda/task7-compliance-monitor \
  --follow
```

## Find EC2 Instances Missing a Specific Tag

```bash
aws ec2 describe-instances \
  --region ap-south-1 \
  --query 'Reservations[].Instances[].[InstanceId,Tags]'
```

## List Unencrypted EBS Volumes

```bash
aws ec2 describe-volumes \
  --region ap-south-1 \
  --filters Name=encrypted,Values=false \
  --query 'Volumes[].[VolumeId,State,Size]'
```

## List IAM Users

```bash
aws iam list-users
```

## List Access Keys

```bash
aws iam list-access-keys \
  --user-name <USER_NAME>
```

## List SNS Subscriptions

```bash
aws sns list-subscriptions-by-topic \
  --topic-arn <SNS_TOPIC_ARN>
```
