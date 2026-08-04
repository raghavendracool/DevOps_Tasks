#!/bin/bash
set -euo pipefail

STACK_NAME="${1:-task15-two-tier-web}"

aws cloudformation delete-stack \
  --stack-name "${STACK_NAME}"

echo "Waiting for stack deletion..."
aws cloudformation wait stack-delete-complete \
  --stack-name "${STACK_NAME}"

echo "Stack ${STACK_NAME} deleted."
