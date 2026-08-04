#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="${ROOT_DIR}/cloudformation/template.yaml"

aws cloudformation validate-template \
  --template-body "file://${TEMPLATE}"

if command -v cfn-lint >/dev/null 2>&1; then
  cfn-lint "${TEMPLATE}"
else
  echo "cfn-lint is not installed; AWS validate-template completed."
fi
