#!/usr/bin/env python3
"""
=============================================================================
  Cross-Platform Developer & System Cache Cleaner (Windows & macOS & Linux)
  Author: tahakdgn
  License: MIT
=============================================================================
  Safely scans and cleans temporary developer caches, build artifacts, 
  and system temp files without removing your personal code or projects.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Terminal ANSI Colors
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

def get_folder_size(path: Path) -> int:
    """Recursively calculates directory size in bytes."""
    total = 0
    if not path.exists():
        return 0
    try:
        if path.is_file() or path.is_symlink():
            return path.stat().st_size
        for entry in path.rglob('*'):
            try:
                if entry.is_file() and not entry.is_symlink():
                    total += entry.stat().st_size
            except (PermissionError, FileNotFoundError, OSError):
                continue
    except (PermissionError, FileNotFoundError, OSError):
        pass
    return total

def format_size(bytes_val: int) -> str:
    """Formats bytes into human readable KB, MB, or GB."""
    if bytes_val >= 1073741824:  # 1 GB
        return f"{bytes_val / 1073741824:.2f} GB"
    elif bytes_val >= 1048576:   # 1 MB
        return f"{bytes_val / 1048576:.2f} MB"
    elif bytes_val >= 1024:      # 1 KB
        return f"{bytes_val / 1024:.2f} KB"
    else:
        return f"{bytes_val} B"

def run_cli_command(cmd, description):
    """Executes a CLI command silently if available."""
    print(f"{GRAY}Running {description}... {RESET}", end="", flush=True)
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            print(f"{GREEN}SUCCESS{RESET}")
        else:
            print(f"{YELLOW}SKIPPED / NOT INSTALLED{RESET}")
    except Exception:
        print(f"{YELLOW}SKIPPED{RESET}")

def get_target_directories():
    """Returns target cache paths based on current OS."""
    home = Path.home()
    system = platform.system()

    targets = []

    if system == "Windows":
        local_app_data = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
        app_data = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
        temp_dir = Path(os.environ.get("TEMP", local_app_data / "Temp"))

        targets = [
            ("User Temp (%TEMP%)", temp_dir, "System", "Temporary application files"),
            ("System Temp (C:\\Windows\\Temp)", Path("C:\\Windows\\Temp"), "System", "Windows OS temp files"),
            ("Gradle Cache", home / ".gradle" / "caches", "Dev", "Android / Java build cache"),
            ("NPM Cache", local_app_data / "npm-cache", "Dev", "Node.js package cache"),
            ("Yarn Cache", local_app_data / "Yarn" / "Cache", "Dev", "Yarn package cache"),
            ("Flutter / Pub Cache", local_app_data / "Pub" / "Cache", "Dev", "Flutter package cache"),
            ("Pip Cache", local_app_data / "pip" / "cache", "Dev", "Python package cache"),
            ("NuGet Cache", home / ".nuget" / "packages", "Dev", ".NET package cache"),
            ("VS Code Cache", app_data / "Code" / "Cache", "Dev", "VS Code cache"),
            ("VS Code CachedData", app_data / "Code" / "CachedData", "Dev", "VS Code JS/TS cache"),
            ("VS Code GPU Cache", app_data / "Code" / "GPUCache", "Dev", "VS Code rendering cache"),
            ("Android SDK Temp", local_app_data / "Android" / "Sdk" / "temp", "Dev", "Android SDK temp downloads"),
        ]
    elif system == "Darwin":  # macOS
        library = home / "Library"
        caches = library / "Caches"

        targets = [
            ("User Caches (~/Library/Caches)", caches, "System", "macOS app cache directory"),
            ("Xcode DerivedData", library / "Developer" / "Xcode" / "DerivedData", "Dev", "Xcode build index & binaries"),
            ("Xcode Archives", library / "Developer" / "Xcode" / "Archives", "Dev", "Xcode archive build outputs"),
            ("CocoaPods Cache", caches / "CocoaPods", "Dev", "iOS pod dependency cache"),
            ("Gradle Cache", home / ".gradle" / "caches", "Dev", "Android / Java build cache"),
            ("NPM Cache", home / ".npm" / "_cacache", "Dev", "Node.js npm cache"),
            ("Yarn Cache", caches / "Yarn", "Dev", "Yarn package cache"),
            ("Flutter / Pub Cache", home / ".pub-cache", "Dev", "Flutter package cache"),
            ("Homebrew Cache", caches / "Homebrew", "Dev", "Homebrew formula downloads"),
            ("Pip Cache", caches / "pip", "Dev", "Python package cache"),
            ("VS Code Cache", caches / "com.microsoft.VSCode", "Dev", "VS Code macOS cache"),
            ("Android SDK Temp", library / "Android" / "sdk" / "temp", "Dev", "Android SDK temp downloads"),
        ]
    else:  # Linux / Unix
        caches = home / ".cache"
        targets = [
            ("User Cache (~/.cache)", caches, "System", "Linux cache directory"),
            ("Gradle Cache", home / ".gradle" / "caches", "Dev", "Android / Java build cache"),
            ("NPM Cache", home / ".npm", "Dev", "Node.js package cache"),
            ("Pub Cache", home / ".pub-cache", "Dev", "Flutter package cache"),
            ("Pip Cache", caches / "pip", "Dev", "Python package cache"),
        ]

    return targets, system

def clean_directory(path: Path) -> int:
    """Safely deletes contents of a directory, returning bytes freed."""
    freed = 0
    if not path.exists():
        return 0

    for item in path.glob('*'):
        try:
            if item.is_file() or item.is_symlink():
                size = item.stat().st_size
                item.unlink()
                freed += size
            elif item.is_dir():
                size = get_folder_size(item)
                shutil.rmtree(item, ignore_errors=True)
                freed += size
        except Exception:
            # Locked files or permission errors will be skipped safely
            continue

    return freed

def run_mac_extra_cleanups():
    """Executes macOS specific CLI tools for Simulator & CocoaPods & Flutter."""
    print(f"\n{BOLD}{CYAN}--- Running macOS Helper Tools ---{RESET}")
    # 1. CocoaPods CLI clean
    run_cli_command("pod cache clean --all", "CocoaPods Cache Clean (pod cache clean --all)")
    # 2. iOS Simulators unavailable clean
    run_cli_command("xcrun simctl delete unavailable", "Deleting Unavailable iOS Simulators")

def main():
    targets, current_os = get_target_directories()

    print(f"\n{CYAN}========================================================================={RESET}")
    print(f"{BOLD}{YELLOW}   DEV & SYSTEM CACHE CLEANER - {current_os.upper()} VERSION{RESET}")
    print(f"{CYAN}========================================================================={RESET}\n")

    print(f"{GRAY}Scanning cache directories... Please wait...{RESET}\n")

    scanned = []
    total_bytes = 0

    for name, path, category, desc in targets:
        if path.exists():
            size = get_folder_size(path)
            total_bytes += size
            scanned.append({
                "name": name,
                "path": path,
                "category": category,
                "desc": desc,
                "size": size,
                "formatted": format_size(size),
                "exists": True
            })
        else:
            scanned.append({
                "name": name,
                "path": path,
                "category": category,
                "desc": desc,
                "size": 0,
                "formatted": "Not Found",
                "exists": False
            })

    # Header
    print(f"{BOLD}{CYAN}{'Cache Name':<28} | {'Cat':<6} | {'Size':>12} | {'Description'}{RESET}")
    print(f"{GRAY}{'-' * 85}{RESET}")

    for item in scanned:
        if item["exists"] and item["size"] > 0:
            color = YELLOW if item["category"] == "Dev" else GREEN
            print(f"{color}{item['name']:<28} | {item['category']:<6} | {item['formatted']:>12} | {item['desc']}{RESET}")
        else:
            print(f"{GRAY}{item['name']:<28} | {item['category']:<6} | {item['formatted']:>12} | {item['desc']}{RESET}")

    print(f"{GRAY}{'-' * 85}{RESET}")
    print(f"{BOLD}{YELLOW}TOTAL CLEANABLE SPACE: {format_size(total_bytes)}{RESET}\n")

    if total_bytes == 0:
        print(f"{GREEN}System is already squeaky clean! No caches to clear.{RESET}\n")
        if current_os == "Darwin":
            run_mac_extra_cleanups()
        return

    # Check for auto-clean argument
    auto_confirm = "--force" in sys.argv or "-y" in sys.argv

    if not auto_confirm:
        confirm = input(f"{BOLD}{RED}Do you want to clean all the caches listed above? (y/N): {RESET}").strip().lower()
        if confirm != 'y':
            print(f"{GRAY}Operation cancelled by user.{RESET}\n")
            return

    print(f"\n{CYAN}Starting cleanup process...{RESET}\n")
    total_freed = 0

    for item in scanned:
        if item["exists"] and item["size"] > 0:
            print(f"{GRAY}Cleaning {item['name']}... {RESET}", end="", flush=True)
            freed = clean_directory(item["path"])
            total_freed += freed
            print(f"{GREEN}DONE! (Freed {format_size(freed)}){RESET}")

    if current_os == "Darwin":
        run_mac_extra_cleanups()

    print(f"\n{CYAN}========================================================================={RESET}")
    print(f"{BOLD}{GREEN}CLEANUP COMPLETE! Total Freed Space: {format_size(total_freed)}{RESET}")
    print(f"{CYAN}========================================================================={RESET}\n")

if __name__ == "__main__":
    main()
