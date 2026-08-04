# Part 3 — Flask Application Setup

[← Part 2](README_PART2.md) | [Next: Part 4 →](README_PART4.md)

## Application Files

```text
app/
├── app.py
├── requirements.txt
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
└── static/
    └── style.css
```

## Step 1 — Install Locally

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 2 — Configure Environment Variables

```bash
export S3_BUCKET_NAME="<BUCKET_NAME>"
export AWS_REGION="ap-south-1"
export FLASK_SECRET_KEY="replace-with-a-long-random-secret"
```

## Step 3 — Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Application Flow

1. User registers.
2. Password is hashed.
3. User logs in.
4. Session stores the authenticated user.
5. Uploaded objects are stored under:

```text
users/<username>/<filename>
```

6. Dashboard lists only that user prefix.
7. Download checks the prefix before returning data.
8. Delete checks ownership before deleting.

## Important Note

The sample stores users in SQLite for demonstration.

Production improvement:

- Amazon RDS
- Amazon Cognito
- DynamoDB
- Secrets Manager

## Checklist

- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Registration works
- [ ] Login works
- [ ] Upload works
- [ ] List works
- [ ] Download works
- [ ] Delete works
