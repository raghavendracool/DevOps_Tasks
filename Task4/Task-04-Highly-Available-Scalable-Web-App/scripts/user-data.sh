#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y apache2 curl stress-ng

systemctl enable apache2
systemctl start apache2

# Use EC2 Instance Metadata Service v2.
TOKEN=$(curl -sS -X PUT \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
  http://169.254.169.254/latest/api/token)

INSTANCE_ID=$(curl -sS \
  -H "X-aws-ec2-metadata-token: ${TOKEN}" \
  http://169.254.169.254/latest/meta-data/instance-id)

LOCAL_HOSTNAME=$(curl -sS \
  -H "X-aws-ec2-metadata-token: ${TOKEN}" \
  http://169.254.169.254/latest/meta-data/local-hostname)

AVAILABILITY_ZONE=$(curl -sS \
  -H "X-aws-ec2-metadata-token: ${TOKEN}" \
  http://169.254.169.254/latest/meta-data/placement/availability-zone)

cat > /var/www/html/index.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Highly Available AWS Web Application</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #102a56, #2563eb);
      color: #172033;
      min-height: 100vh;
      display: grid;
      place-items: center;
    }
    .card {
      width: min(760px, 88%);
      background: white;
      padding: 42px;
      border-radius: 18px;
      box-shadow: 0 20px 45px rgba(0,0,0,.25);
      text-align: center;
    }
    h1 { color: #102a56; }
    .instance {
      margin: 28px 0;
      padding: 20px;
      border: 2px solid #f59e0b;
      background: #fff7ed;
      border-radius: 12px;
      font-size: 20px;
    }
    .label { font-weight: bold; color: #9a3412; }
  </style>
</head>
<body>
  <main class="card">
    <h1>Highly Available AWS Web Application</h1>
    <p>This page is served by an Ubuntu EC2 instance behind an Application Load Balancer.</p>
    <section class="instance">
      <p><span class="label">Instance ID:</span> ${INSTANCE_ID}</p>
      <p><span class="label">Private Hostname:</span> ${LOCAL_HOSTNAME}</p>
      <p><span class="label">Availability Zone:</span> ${AVAILABILITY_ZONE}</p>
    </section>
    <p>Refresh the ALB URL to observe traffic distribution across healthy targets.</p>
  </main>
</body>
</html>
EOF

chown root:root /var/www/html/index.html
chmod 644 /var/www/html/index.html

apache2ctl configtest
systemctl restart apache2
