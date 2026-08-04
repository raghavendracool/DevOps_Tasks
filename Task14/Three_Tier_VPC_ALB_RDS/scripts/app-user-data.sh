#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y nginx python3-pip python3-venv git mysql-client curl

mkdir -p /opt/task14/app/templates /opt/task14/app/static
python3 -m venv /opt/task14/venv
/opt/task14/venv/bin/pip install Flask==3.1.1 PyMySQL==1.1.1 gunicorn==23.0.0

cat > /opt/task14/app/app.py <<'PYEOF'
# Replace with application/app.py from the repository.
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Task 14 application placeholder"

@app.route("/health")
def health():
    return {"status": "healthy"}
PYEOF

cat > /etc/systemd/system/task14-app.service <<'EOF'
[Unit]
Description=Task 14 Application
After=network-online.target

[Service]
User=ubuntu
WorkingDirectory=/opt/task14/app
EnvironmentFile=-/etc/task14-app.env
ExecStart=/opt/task14/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/nginx/sites-available/task14 <<'EOF'
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

ln -sf /etc/nginx/sites-available/task14 /etc/nginx/sites-enabled/task14
rm -f /etc/nginx/sites-enabled/default

systemctl daemon-reload
systemctl enable task14-app nginx
systemctl restart task14-app nginx
