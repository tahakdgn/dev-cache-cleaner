@echo off
title Windows & macOS Dev Cache Cleaner
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% equ 0 (
    python clean.py
) else (
    where python3 >nul 2>nul
    if %errorlevel% equ 0 (
        python3 clean.py
    ) else (
        echo [!] Python 3 not found on PATH. Please install Python 3.
    )
)

pause
