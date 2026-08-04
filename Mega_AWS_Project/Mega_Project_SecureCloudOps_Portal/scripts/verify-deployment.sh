#!/bin/bash
set -euo pipefail
ALB="${1:?Usage: $0 <alb-dns-name>}"
echo "Checking ALB..."
curl -fsS "http://${ALB}/health"
echo
curl -fsS "http://${ALB}/api/health/db"
echo
echo "Deployment verification passed."
