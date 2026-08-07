@echo off
title Windows Dev Cache Cleaner CLI
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% equ 0 (
    python "%~dp0..\core\clean.py"
) else (
    where python3 >nul 2>nul
    if %errorlevel% equ 0 (
        python3 "%~dp0..\core\clean.py"
    ) else (
        echo [!] Python 3 is required. Please install Python 3.
        pause
    )
)

pause
