#!/bin/bash
set -euo pipefail

echo "=== Hostname ==="
hostname

echo
echo "=== IP Addresses ==="
hostname -I

echo
echo "=== Routes ==="
ip route

echo
echo "=== SSH Service ==="
sudo systemctl status ssh --no-pager || true

echo
echo "=== Internet Test ==="
curl -I --max-time 10 https://aws.amazon.com || true

echo
echo "=== Public Egress IP ==="
curl -s --max-time 10 https://checkip.amazonaws.com || true
echo
