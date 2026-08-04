#!/bin/bash
set -euo pipefail

FUNCTION_NAME="${1:-task7-compliance-monitor}"

cd "$(dirname "$0")/../lambda"
zip -j /tmp/task7-compliance-monitor.zip lambda_function.py

aws lambda update-function-code \
  --function-name "${FUNCTION_NAME}" \
  --zip-file fileb:///tmp/task7-compliance-monitor.zip

aws lambda update-function-configuration \
  --function-name "${FUNCTION_NAME}" \
  --timeout 30

echo "Deployed ${FUNCTION_NAME} with a 30-second timeout."
