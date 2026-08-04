import os
import sys

import pymysql

required = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
missing = [name for name in required if not os.getenv(name)]

if missing:
    print(f"Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

connection = None

try:
    connection = pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        connect_timeout=10,
        ssl={"ca": os.getenv("DB_SSL_CA", "/etc/ssl/certs/global-bundle.pem")},
    )

    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION(), DATABASE(), CURRENT_USER()")
        result = cursor.fetchone()

    print("Database connection successful")
    print(f"MySQL version : {result[0]}")
    print(f"Database      : {result[1]}")
    print(f"Connected user: {result[2]}")

except Exception as exc:
    print(f"Database connection failed: {exc}")
    sys.exit(2)

finally:
    if connection:
        connection.close()
