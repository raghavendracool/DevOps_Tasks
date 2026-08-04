import os
import socket
from datetime import datetime

import pymysql
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
INSTANCE_NAME = os.getenv("INSTANCE_NAME", socket.gethostname())


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5,
        autocommit=True,
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
        instance_name=INSTANCE_NAME,
        hostname=socket.gethostname(),
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "instance": INSTANCE_NAME,
    })


@app.route("/api/db")
def db_health():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION(), NOW()")
            row = cursor.fetchone()
        connection.close()
        return jsonify({
            "status": "connected",
            "mysql_version": row[0],
            "database_time": str(row[1]),
            "instance": INSTANCE_NAME,
        })
    except Exception as exc:
        app.logger.exception("Database connection failed")
        return jsonify({
            "status": "failed",
            "error": str(exc),
            "instance": INSTANCE_NAME,
        }), 503


@app.route("/visit", methods=["POST"])
def create_visit():
    visitor = request.form.get("visitor", "anonymous").strip()[:100]

    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO visits (visitor_name, served_by)
            VALUES (%s, %s)
            """,
            (visitor, INSTANCE_NAME),
        )
    connection.close()

    return index()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
