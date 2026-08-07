@echo off
title Windows Dev Cache Cleaner
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% equ 0 (
    start "" pythonw "%~dp0..\core\gui.py"
) else (
    where python3 >nul 2>nul
    if %errorlevel% equ 0 (
        start "" pythonw3 "%~dp0..\core\gui.py"
    ) else (
        echo [!] Python 3 is required. Please install Python 3.
        pause
    )
)
