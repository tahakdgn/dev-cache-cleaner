#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/../core"

echo "================================================================="
echo "   Launching Dev & System Cache Cleaner GUI for macOS...        "
echo "================================================================="
echo ""

PYTHON_BIN=""

if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "[!] Error: Python is not installed."
    echo "[!] Please install Python from https://www.python.org or via Homebrew (brew install python)"
    echo ""
    read -p "Press [Enter] key to close..."
    exit 1
fi

# Check if tkinter module is available
$PYTHON_BIN -c "import tkinter" &>/dev/null

if [ $? -eq 0 ]; then
    echo "[+] Tkinter detected. Opening Graphical User Interface..."
    $PYTHON_BIN gui.py
else
    echo "[!] Note: Tkinter GUI module is not included in this Python build."
    echo "[+] Running interactive CLI mode instead..."
    echo ""
    $PYTHON_BIN clean.py
fi

echo ""
read -p "Press [Enter] key to close..."
