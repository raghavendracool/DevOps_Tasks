#!/bin/bash
set -euo pipefail

FUNCTION_NAME="${1:-task9-unauthorized-iam-user-alert}"

cd "$(dirname "$0")/../lambda"
zip -j /tmp/task9-security-monitor.zip lambda_function.py

aws lambda update-function-code \
  --function-name "${FUNCTION_NAME}" \
  --zip-file fileb:///tmp/task9-security-monitor.zip

echo "Updated ${FUNCTION_NAME}"
