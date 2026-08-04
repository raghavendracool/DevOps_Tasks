# Task 8 — AWS CLI Cheat Sheet

## List User Files

```bash
aws s3 ls s3://<BUCKET_NAME>/users/raghav/ --recursive
```

## Upload

```bash
aws s3 cp report.pdf \
  s3://<BUCKET_NAME>/users/raghav/report.pdf
```

## Download

```bash
aws s3 cp \
  s3://<BUCKET_NAME>/users/raghav/report.pdf \
  .
```

## Enable Versioning

```bash
aws s3api put-bucket-versioning \
  --bucket <BUCKET_NAME> \
  --versioning-configuration Status=Enabled
```

## Check Public Access Block

```bash
aws s3api get-public-access-block \
  --bucket <BUCKET_NAME>
```

## Check EC2 IAM Role

```bash
aws sts get-caller-identity
```
