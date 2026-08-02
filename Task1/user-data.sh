#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y nginx curl

systemctl enable nginx
systemctl start nginx

TOKEN=$(curl -sS -X PUT \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
  http://169.254.169.254/latest/api/token)

INSTANCE_ID=$(curl -sS \
  -H "X-aws-ec2-metadata-token: ${TOKEN}" \
  http://169.254.169.254/latest/meta-data/instance-id)

AZ=$(curl -sS \
  -H "X-aws-ec2-metadata-token: ${TOKEN}" \
  http://169.254.169.254/latest/meta-data/placement/availability-zone)

LOCAL_IPV4=$(curl -sS \
  -H "X-aws-ec2-metadata-token: ${TOKEN}" \
  http://169.254.169.254/latest/meta-data/local-ipv4)

HOST_NAME=$(hostname)

cat > /var/www/html/index.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-AZ Ubuntu Web Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 40px;
            text-align: center;
        }

        .container {
            max-width: 760px;
            margin: auto;
            background: white;
            padding: 35px;
            border-radius: 12px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.12);
        }

        h1 {
            color: #e95420;
        }

        table {
            margin: 25px auto;
            border-collapse: collapse;
            width: 90%;
        }

        th, td {
            border: 1px solid #dddddd;
            padding: 12px;
        }

        th {
            background: #e95420;
            color: white;
        }

        .status {
            color: green;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Ubuntu Multi-AZ Web Server</h1>
        <p class="status">NGINX is running successfully</p>

        <table>
            <tr>
                <th>Property</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Hostname</td>
                <td>${HOST_NAME}</td>
            </tr>
            <tr>
                <td>Instance ID</td>
                <td>${INSTANCE_ID}</td>
            </tr>
            <tr>
                <td>Availability Zone</td>
                <td>${AZ}</td>
            </tr>
            <tr>
                <td>Private IP</td>
                <td>${LOCAL_IPV4}</td>
            </tr>
            <tr>
                <td>Operating System</td>
                <td>Ubuntu Server</td>
            </tr>
        </table>
    </div>
</body>
</html>
EOF

nginx -t
systemctl restart nginx
