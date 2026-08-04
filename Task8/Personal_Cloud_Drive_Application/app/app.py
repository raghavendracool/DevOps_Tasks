import io
import os
import sqlite3
from functools import wraps

import boto3
from botocore.exceptions import ClientError
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-me")
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

BUCKET_NAME = os.environ["S3_BUCKET_NAME"]
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
DATABASE = os.getenv("DATABASE_PATH", "users.db")

s3 = boto3.client("s3", region_name=AWS_REGION)

ALLOWED_EXTENSIONS = {
    "txt", "pdf", "doc", "docx", "xls", "xlsx", "csv",
    "png", "jpg", "jpeg", "gif", "zip", "mp4", "mp3"
}


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def user_prefix(username):
    return f"users/{username}/"


@app.route("/")
def index():
    return redirect(url_for("dashboard" if "username" in session else "login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("register"))

        connection = get_db()
        try:
            connection.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists.")
            return redirect(url_for("register"))
        finally:
            connection.close()

        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        connection = get_db()
        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        connection.close()

        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.")
            return redirect(url_for("login"))

        session.clear()
        session["username"] = username
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    prefix = user_prefix(session["username"])
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    files = []

    for item in response.get("Contents", []):
        key = item["Key"]
        if key == prefix:
            continue
        files.append({
            "name": key[len(prefix):],
            "size": item["Size"],
            "last_modified": item["LastModified"],
        })

    return render_template("dashboard.html", files=files, username=session["username"])


@app.route("/upload", methods=["POST"])
@login_required
def upload():
    uploaded_file = request.files.get("file")

    if not uploaded_file or not uploaded_file.filename:
        flash("Select a file.")
        return redirect(url_for("dashboard"))

    filename = secure_filename(uploaded_file.filename)

    if not filename or not allowed_file(filename):
        flash("File type is not allowed.")
        return redirect(url_for("dashboard"))

    key = f"{user_prefix(session['username'])}{filename}"

    s3.upload_fileobj(
        uploaded_file,
        BUCKET_NAME,
        key,
        ExtraArgs={
            "ServerSideEncryption": "AES256",
            "ContentType": uploaded_file.content_type or "application/octet-stream",
        },
    )

    flash("File uploaded successfully.")
    return redirect(url_for("dashboard"))


@app.route("/download/<path:filename>")
@login_required
def download(filename):
    safe_name = secure_filename(filename)
    key = f"{user_prefix(session['username'])}{safe_name}"

    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") in {"NoSuchKey", "404"}:
            flash("File not found.")
            return redirect(url_for("dashboard"))
        raise

    return send_file(
        io.BytesIO(response["Body"].read()),
        as_attachment=True,
        download_name=safe_name,
        mimetype=response.get("ContentType", "application/octet-stream"),
    )


@app.route("/delete/<path:filename>", methods=["POST"])
@login_required
def delete(filename):
    safe_name = secure_filename(filename)
    key = f"{user_prefix(session['username'])}{safe_name}"
    s3.delete_object(Bucket=BUCKET_NAME, Key=key)
    flash("File deleted.")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
