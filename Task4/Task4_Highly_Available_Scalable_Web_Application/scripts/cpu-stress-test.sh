#!/bin/bash
set -euo pipefail

DURATION="${1:-15m}"
LOAD="${2:-100}"
CPU_WORKERS="$(nproc)"

echo "Starting CPU stress test"
echo "Workers : ${CPU_WORKERS}"
echo "Load    : ${LOAD}%"
echo "Duration: ${DURATION}"

stress-ng \
  --cpu "${CPU_WORKERS}" \
  --cpu-load "${LOAD}" \
  --timeout "${DURATION}" \
  --metrics-brief
