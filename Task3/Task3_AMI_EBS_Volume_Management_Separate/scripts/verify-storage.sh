#!/bin/bash
set -euo pipefail
lsblk -f
df -hT
findmnt /data || true
cat /data/verification.txt 2>/dev/null || true
