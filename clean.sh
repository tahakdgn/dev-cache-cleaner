#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

if command -v python3 &>/dev/null; then
    python3 clean.py "$@"
elif command -v python &>/dev/null; then
    python clean.py "$@"
else
    echo "Python 3 is required."
    exit 1
fi
