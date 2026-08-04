# Part 2 — S3 Bucket, Folder Design and Test Files

[← Part 1](README_PART1.md) | [Next: Part 3 →](README_PART3.md)

## Step 1 — Create the S3 Bucket

Open:

```text
Amazon S3 → Create bucket
```

Configure:

```text
Bucket name: raghav-task6-file-classifier-<unique>
Region: ap-south-1
Block Public Access: Keep enabled
Versioning: Optional but recommended
Default encryption: SSE-S3
```

## Step 2 — Create Prefixes

Create these folders:

```text
incoming/
Finance/
Non-Finance/
```

S3 folders are logical prefixes.

## Step 3 — Prepare Test Files

The ZIP includes:

```text
test-files/
├── fin_budget.txt
├── fin_q1_report.csv
├── employee_list.csv
└── project_notes.txt
```

Expected classification:

| File | Destination |
|---|---|
| `fin_budget.txt` | `Finance/` |
| `fin_q1_report.csv` | `Finance/` |
| `employee_list.csv` | `Non-Finance/` |
| `project_notes.txt` | `Non-Finance/` |

## Step 4 — Upload Files Later to `incoming/`

Do not upload before the Lambda trigger is configured unless you plan to re-upload them.

AWS CLI example:

```bash
aws s3 cp fin_budget.txt \
  s3://<BUCKET_NAME>/incoming/fin_budget.txt

aws s3 cp employee_list.csv \
  s3://<BUCKET_NAME>/incoming/employee_list.csv
```

## Optional Versioning

Enable versioning:

```bash
aws s3api put-bucket-versioning \
  --bucket <BUCKET_NAME> \
  --versioning-configuration Status=Enabled
```

Versioning helps recover accidentally deleted objects.

## Optional Lifecycle Rule

For a training project, you can automatically delete old test files after a few days.

Do not use lifecycle deletion in production without approval.

## Checklist

- [ ] Bucket created
- [ ] Block Public Access enabled
- [ ] Encryption enabled
- [ ] Prefixes created
- [ ] Test files prepared
- [ ] Bucket name recorded
