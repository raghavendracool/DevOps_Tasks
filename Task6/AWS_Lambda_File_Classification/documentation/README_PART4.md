# Part 4 — S3 Event Notification, Testing and Monitoring

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Step 1 — Add the S3 Trigger

Open:

```text
Lambda → task6-file-classifier → Add trigger
```

Choose:

```text
Source: S3
Bucket: <BUCKET_NAME>
Event type: All object create events
Prefix: incoming/
Suffix: Leave empty
Recursive invocation warning: Acknowledge
```

The `incoming/` prefix is critical.

## Step 2 — Upload Finance Files

```bash
aws s3 cp test-files/fin_budget.txt \
  s3://<BUCKET_NAME>/incoming/fin_budget.txt

aws s3 cp test-files/fin_q1_report.csv \
  s3://<BUCKET_NAME>/incoming/fin_q1_report.csv
```

Expected:

```text
Finance/fin_budget.txt
Finance/fin_q1_report.csv
```

## Step 3 — Upload Non-Finance Files

```bash
aws s3 cp test-files/employee_list.csv \
  s3://<BUCKET_NAME>/incoming/employee_list.csv

aws s3 cp test-files/project_notes.txt \
  s3://<BUCKET_NAME>/incoming/project_notes.txt
```

Expected:

```text
Non-Finance/employee_list.csv
Non-Finance/project_notes.txt
```

## Step 4 — Verify the Source Prefix

After successful processing, the original object should be removed from:

```text
incoming/
```

List objects:

```bash
aws s3 ls s3://<BUCKET_NAME>/ --recursive
```

## Step 5 — Check CloudWatch Logs

Open:

```text
CloudWatch → Log groups → /aws/lambda/task6-file-classifier
```

Look for:

```text
Classified incoming/fin_budget.txt as Finance/fin_budget.txt
Classified incoming/employee_list.csv as Non-Finance/employee_list.csv
```

## Step 6 — Monitor Lambda Metrics

Check:

- Invocations
- Errors
- Duration
- Throttles
- Concurrent executions

## Optional Dead-Letter or Failure Destination

For production, configure:

- Lambda asynchronous failure destination to Amazon SQS or SNS
- CloudWatch alarm for Lambda errors
- S3 EventBridge integration for more advanced routing

## Important Event Behavior

S3 event notifications are generally delivered at least once.

Your function should be idempotent and safe when the same event is delivered more than once.

The supplied code checks whether the source object still exists before processing.

## Checklist

- [ ] S3 trigger added
- [ ] Prefix filter is `incoming/`
- [ ] Finance files tested
- [ ] Non-Finance files tested
- [ ] Source objects removed
- [ ] CloudWatch logs checked
- [ ] Lambda errors are zero
