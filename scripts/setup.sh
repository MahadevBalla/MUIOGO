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

# Find a suitable Python 3 interpreter
PYTHON=""
for candidate in python3 python; do
    if command -v "$candidate" &>/dev/null; then
        version=$("$candidate" -c "import sys; print(sys.version_info >= (3, 9))" 2>/dev/null || echo "False")
        if [ "$version" = "True" ]; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "ERROR: Python 3.9+ is required but not found in PATH."
    echo "Install Python from https://www.python.org/downloads/ and try again."
    exit 1
fi

echo "Using Python: $($PYTHON --version) at $(command -v $PYTHON)"

exec "$PYTHON" "$SCRIPT_DIR/setup_dev.py" "$@"
