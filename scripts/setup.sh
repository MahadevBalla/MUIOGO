#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# MUIOGO Development Environment Setup (macOS / Linux)
#
# Usage:
#   ./scripts/setup.sh          # full setup
#   ./scripts/setup.sh --check  # verification only
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Find a suitable Python 3 interpreter (supported range: >=3.10,<3.13)
PYTHON=""
for candidate in python3.12 python3.11 python3.10 python3 python; do
    if command -v "$candidate" &>/dev/null; then
        version=$("$candidate" -c "import sys; print((3, 10) <= sys.version_info[:2] < (3, 13))" 2>/dev/null || echo "False")
        if [ "$version" = "True" ]; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "ERROR: A supported Python interpreter was not found in PATH."
    echo "MUIOGO setup currently supports Python >=3.10 and <3.13 (recommended: 3.11)."
    exit 1
fi

echo "Using Python: $($PYTHON --version) at $(command -v $PYTHON)"

exec "$PYTHON" "$SCRIPT_DIR/setup_dev.py" "$@"
