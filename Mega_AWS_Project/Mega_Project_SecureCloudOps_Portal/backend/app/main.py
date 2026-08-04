import os
import socket
import uuid
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
import boto3
from botocore.exceptions import ClientError

from .auth import create_token, current_user, hash_password, verify_password
from .config import settings
from .database import Base, engine, get_db
from .models import FileObject, User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureCloudOps API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
s3 = boto3.client("s3", region_name=settings.aws_region)

@app.get("/health")
def health():
    return {"status": "healthy", "hostname": socket.gethostname()}

@app.get("/api/health/db")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "connected"}

@app.get("/api/instance")
def instance():
    return {"hostname": socket.gethostname(), "instance_name": os.getenv("INSTANCE_NAME", "local")}

@app.post("/api/auth/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    username = username.strip().lower()
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(409, "Username already exists")
    user = User(username=username, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "registered"}

@app.post("/api/auth/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username.strip().lower()).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_token(user.id), "token_type": "bearer"}

@app.get("/api/files")
def list_files(user: User = Depends(current_user), db: Session = Depends(get_db)):
    rows = db.query(FileObject).filter(FileObject.owner_id == user.id).order_by(FileObject.created_at.desc()).all()
    return [
        {
            "id": row.id,
            "name": row.original_name,
            "classification": row.classification,
            "size_bytes": row.size_bytes,
            "created_at": row.created_at,
        }
        for row in rows
    ]

@app.post("/api/files/upload")
def upload_file(
    upload: UploadFile = File(...),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    safe_name = upload.filename.replace("/", "_").replace("\\", "_")
    key = f"uploads/{user.id}/{uuid.uuid4()}-{safe_name}"
    s3.upload_fileobj(
        upload.file,
        settings.s3_bucket_name,
        key,
        ExtraArgs={"ServerSideEncryption": "AES256", "ContentType": upload.content_type or "application/octet-stream"},
    )
    row = FileObject(owner_id=user.id, original_name=safe_name, s3_key=key, size_bytes=0)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "key": key, "classification": "pending"}

@app.get("/api/files/{file_id}/download")
def download_file(file_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    row = db.get(FileObject, file_id)
    if not row or row.owner_id != user.id:
        raise HTTPException(404, "File not found")
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.s3_bucket_name, "Key": row.s3_key},
        ExpiresIn=300,
    )
    return {"url": url}

@app.delete("/api/files/{file_id}")
def delete_file(file_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    row = db.get(FileObject, file_id)
    if not row or row.owner_id != user.id:
        raise HTTPException(404, "File not found")
    try:
        s3.delete_object(Bucket=settings.s3_bucket_name, Key=row.s3_key)
    except ClientError:
        pass
    db.delete(row)
    db.commit()
    return {"message": "deleted"}
