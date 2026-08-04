#!/usr/bin/env bash
set -euo pipefail

DURATION="${1:-600}"
CPU_WORKERS="${2:-2}"

echo "Starting CPU load with ${CPU_WORKERS} workers for ${DURATION} seconds..."
sudo stress-ng --cpu "${CPU_WORKERS}" --timeout "${DURATION}s" --metrics-brief
