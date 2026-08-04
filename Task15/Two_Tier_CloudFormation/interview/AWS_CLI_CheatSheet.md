# Task 15 — AWS CLI Cheat Sheet

## Validate

```bash
aws cloudformation validate-template \
  --template-body file://cloudformation/template.yaml
```

## Deploy

```bash
aws cloudformation deploy \
  --template-file cloudformation/template.yaml \
  --stack-name task15-two-tier-web \
  --parameter-overrides \
    KeyName=<KEY_NAME> \
    AdminCidr=<YOUR_IP>/32 \
  --capabilities CAPABILITY_NAMED_IAM
```

## Stack Status

```bash
aws cloudformation describe-stacks \
  --stack-name task15-two-tier-web
```

## Events

```bash
aws cloudformation describe-stack-events \
  --stack-name task15-two-tier-web
```

## Resources

```bash
aws cloudformation list-stack-resources \
  --stack-name task15-two-tier-web
```

## Outputs

```bash
aws cloudformation describe-stacks \
  --stack-name task15-two-tier-web \
  --query 'Stacks[0].Outputs' \
  --output table
```

## Drift

```bash
aws cloudformation detect-stack-drift \
  --stack-name task15-two-tier-web
```

## Delete

```bash
aws cloudformation delete-stack \
  --stack-name task15-two-tier-web
```
