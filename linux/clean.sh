#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/../core"

if command -v python3 &>/dev/null; then
    python3 gui.py "$@"
elif command -v python &>/dev/null; then
    python gui.py "$@"
else
    echo "Python 3 is required."
    exit 1
fi
