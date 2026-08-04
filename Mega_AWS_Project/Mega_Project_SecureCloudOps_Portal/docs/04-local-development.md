# 4. Local Development

## Environment File

Copy:

```bash
cp .env.example .env
```

Update:

```text
DATABASE_URL=mysql+pymysql://appuser:app-password@db:3306/securecloudops
AWS_REGION=ap-south-1
S3_BUCKET_NAME=local-placeholder
JWT_SECRET=replace-me
```

## Start

```bash
docker compose up --build
```

## Test

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/health/db
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
