#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/../core"

if command -v python3 &>/dev/null; then
    python3 clean.py
elif command -v python &>/dev/null; then
    python clean.py
else
    echo "[!] Python 3 is required to run this script on macOS."
    echo "[!] Please install Python via 'brew install python' or from python.org"
fi

echo ""
read -p "Press [Enter] key to close..."
