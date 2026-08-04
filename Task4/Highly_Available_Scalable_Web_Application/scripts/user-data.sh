#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive
REPO_URL="https://github.com/<username>/<repository>.git"
APP_DIR="/opt/project-04-app"
WEB_ROOT="/var/www/html"

apt-get update -y
apt-get install -y apache2 git curl stress-ng

rm -rf "${APP_DIR}"
git clone "${REPO_URL}" "${APP_DIR}"

rm -rf "${WEB_ROOT:?}"/*
cp -R "${APP_DIR}/website/." "${WEB_ROOT}/"

TOKEN=$(curl -sS -X PUT \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
  http://169.254.169.254/latest/api/token)

metadata() {
  curl -sS \
    -H "X-aws-ec2-metadata-token: ${TOKEN}" \
    "http://169.254.169.254/latest/meta-data/$1"
}

INSTANCE_ID=$(metadata instance-id)
AZ=$(metadata placement/availability-zone)
PRIVATE_IP=$(metadata local-ipv4)
HOSTNAME=$(hostname)

cat > "${WEB_ROOT}/server-info.js" <<EOF
window.SERVER_INFO = {
  instanceId: "${INSTANCE_ID}",
  availabilityZone: "${AZ}",
  privateIp: "${PRIVATE_IP}",
  hostname: "${HOSTNAME}"
};
EOF

chown -R www-data:www-data "${WEB_ROOT}"
find "${WEB_ROOT}" -type d -exec chmod 755 {} \;
find "${WEB_ROOT}" -type f -exec chmod 644 {} \;

systemctl enable apache2
systemctl restart apache2
