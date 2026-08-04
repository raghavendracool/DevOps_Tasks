# Task 6 — AWS CLI Cheat Sheet

## Upload Test Files

```bash
aws s3 cp fin_budget.txt \
  s3://<BUCKET_NAME>/incoming/fin_budget.txt

aws s3 cp employee_list.csv \
  s3://<BUCKET_NAME>/incoming/employee_list.csv
```

## List Objects

```bash
aws s3 ls s3://<BUCKET_NAME>/ --recursive
aws s3 ls s3://<BUCKET_NAME>/Finance/
aws s3 ls s3://<BUCKET_NAME>/Non-Finance/
```

## Invoke Lambda Manually

```bash
aws lambda invoke \
  --function-name task6-file-classifier \
  --payload fileb://event.json \
  response.json
```

## View Function Configuration

```bash
aws lambda get-function-configuration \
  --function-name task6-file-classifier
```

## Tail Logs

```bash
aws logs tail \
  /aws/lambda/task6-file-classifier \
  --follow
```

## View S3 Notification Configuration

```bash
aws s3api get-bucket-notification-configuration \
  --bucket <BUCKET_NAME>
```

## Empty Bucket

```bash
aws s3 rm s3://<BUCKET_NAME>/ --recursive
```
