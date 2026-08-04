# Part 3 — Lambda Function, IAM Role and Deployment

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Step 1 — Create the Lambda Function

Open:

```text
AWS Lambda → Create function
```

Configure:

```text
Function name: task6-file-classifier
Runtime: Python 3.12
Architecture: x86_64
Permissions: Create a new role with basic Lambda permissions
```

## Step 2 — Update IAM Permissions

The Lambda execution role needs:

- `s3:GetObject`
- `s3:PutObject`
- `s3:DeleteObject`
- CloudWatch Logs permissions

Use the supplied policy in:

```text
lambda/iam-policy.json
```

Replace:

```text
<BUCKET_NAME>
```

Attach it to:

```text
IAM → Roles → task6-lambda-s3-role
```

## Step 3 — Deploy the Lambda Code

The supplied function is:

```text
lambda/lambda_function.py
```

The logic:

1. Reads S3 event records.
2. URL-decodes the object key.
3. Ignores non-`incoming/` objects.
4. Extracts the filename.
5. Checks whether the filename starts with `fin_`.
6. Copies the object to the correct prefix.
7. Deletes the original object.
8. Logs the result.

## Environment Variables

Configure:

```text
SOURCE_PREFIX=incoming/
FINANCE_PREFIX=Finance/
NON_FINANCE_PREFIX=Non-Finance/
```

## Recommended Lambda Settings

| Setting | Value |
|---|---|
| Memory | 128 MB |
| Timeout | 30 seconds |
| Ephemeral storage | 512 MB |
| Reserved concurrency | Optional |
| Retry behavior | Default asynchronous retry |

## Step 4 — Deploy

Paste the Python code in the Lambda console or upload a ZIP package.

Click:

```text
Deploy
```

## Step 5 — Create a Console Test Event

Use:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "<BUCKET_NAME>"
        },
        "object": {
          "key": "incoming/fin_budget.txt"
        }
      }
    }
  ]
}
```

This test only works when the object already exists.

## Checklist

- [ ] Lambda created
- [ ] Python 3.12 selected
- [ ] IAM policy attached
- [ ] Environment variables configured
- [ ] Code deployed
- [ ] Timeout set
- [ ] Function test prepared
