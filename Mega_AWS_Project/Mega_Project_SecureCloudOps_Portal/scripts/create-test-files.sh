#!/bin/bash
set -euo pipefail
mkdir -p test-files
echo "Finance invoice" > test-files/fin_invoice.txt
echo "General notes" > test-files/project_notes.txt
echo "Created finance and non-finance test files."
