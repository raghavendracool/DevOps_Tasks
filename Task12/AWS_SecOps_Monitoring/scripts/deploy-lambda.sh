#!/bin/bash
set -euo pipefail

FUNCTION_NAME="${1:-task12-secops-compliance-engine}"

cd "$(dirname "$0")/../lambda"
zip -j /tmp/task12-secops.zip lambda_function.py

aws lambda update-function-code \
  --function-name "${FUNCTION_NAME}" \
  --zip-file fileb:///tmp/task12-secops.zip

echo "Updated ${FUNCTION_NAME}"
