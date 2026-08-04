#!/bin/bash
set -euo pipefail

FUNCTION_NAME="${1:-task10-cloudtrail-security-monitor}"

cd "$(dirname "$0")/../lambda"
zip -j /tmp/task10-cloudtrail-security-monitor.zip lambda_function.py

aws lambda update-function-code \
  --function-name "${FUNCTION_NAME}" \
  --zip-file fileb:///tmp/task10-cloudtrail-security-monitor.zip

echo "Updated ${FUNCTION_NAME}"
