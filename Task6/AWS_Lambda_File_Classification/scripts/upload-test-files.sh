#!/bin/bash
set -euo pipefail

BUCKET_NAME="${1:?Usage: $0 <bucket-name>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="${SCRIPT_DIR}/../test-files"

for file in "${TEST_DIR}"/*; do
  aws s3 cp "${file}" "s3://${BUCKET_NAME}/incoming/$(basename "${file}")"
done

echo "Uploaded test files to s3://${BUCKET_NAME}/incoming/"
