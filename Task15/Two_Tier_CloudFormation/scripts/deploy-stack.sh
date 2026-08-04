#!/bin/bash
set -euo pipefail

STACK_NAME="${1:-task15-two-tier-web}"
KEY_NAME="${2:?Usage: $0 <stack-name> <key-name> <admin-cidr>}"
ADMIN_CIDR="${3:?Usage: $0 <stack-name> <key-name> <admin-cidr>}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

aws cloudformation deploy \
  --template-file "${ROOT_DIR}/cloudformation/template.yaml" \
  --stack-name "${STACK_NAME}" \
  --parameter-overrides \
    KeyName="${KEY_NAME}" \
    AdminCidr="${ADMIN_CIDR}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --tags \
    Project=DevOps-Task-15 \
    Environment=Training

aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --query 'Stacks[0].Outputs' \
  --output table
