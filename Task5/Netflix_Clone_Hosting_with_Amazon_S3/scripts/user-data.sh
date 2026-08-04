#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive
REPO_URL="https://github.com/<username>/<repository>.git"
APP_DIR="/opt/netflix-clone"
WEB_ROOT="/var/www/netflix-clone"

apt-get update -y
apt-get install -y nginx git curl

rm -rf "${APP_DIR}"
git clone "${REPO_URL}" "${APP_DIR}"

mkdir -p "${WEB_ROOT}"
rm -rf "${WEB_ROOT:?}"/*
cp -R "${APP_DIR}/website/." "${WEB_ROOT}/"

cat > /etc/nginx/sites-available/netflix-clone <<'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name _;
    root /var/www/netflix-clone;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(css|js|png|jpg|jpeg|gif|svg|ico)$ {
        expires 7d;
        add_header Cache-Control "public";
    }
}
EOF

ln -sf /etc/nginx/sites-available/netflix-clone \
  /etc/nginx/sites-enabled/netflix-clone

rm -f /etc/nginx/sites-enabled/default

chown -R www-data:www-data "${WEB_ROOT}"
find "${WEB_ROOT}" -type d -exec chmod 755 {} \;
find "${WEB_ROOT}" -type f -exec chmod 644 {} \;

nginx -t
systemctl enable nginx
systemctl restart nginx
