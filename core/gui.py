#!/usr/bin/env python3
"""
=============================================================================
  Dev & System Cache Cleaner - GUI (Tkinter Desktop Interface)
  Author: tahakdgn
  License: MIT
=============================================================================
"""

import os
import sys
import shutil
import threading
import platform
import subprocess
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox

# Ensure core directory is on path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from clean import get_target_directories, get_folder_size, format_size, clean_directory, run_cli_command
except ImportError:
    def get_folder_size(path: Path) -> int:
        total = 0
        if not path.exists(): return 0
        try:
            if path.is_file() or path.is_symlink(): return path.stat().st_size
            for entry in path.rglob('*'):
                try:
                    if entry.is_file() and not entry.is_symlink(): total += entry.stat().st_size
                except (PermissionError, FileNotFoundError, OSError): continue
        except (PermissionError, FileNotFoundError, OSError): pass
        return total

    def format_size(bytes_val: int) -> str:
        if bytes_val >= 1073741824: return f"{bytes_val / 1073741824:.2f} GB"
        elif bytes_val >= 1048576: return f"{bytes_val / 1048576:.2f} MB"
        elif bytes_val >= 1024: return f"{bytes_val / 1024:.2f} KB"
        else: return f"{bytes_val} B"

    def clean_directory(path: Path) -> int:
        freed = 0
        if not path.exists(): return 0
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
            except Exception: continue
        return freed

# Colors - Catppuccin Mocha Palette
BG_COLOR = "#1e1e2e"
CARD_BG = "#252538"
HEADER_BG = "#181825"
TEXT_COLOR = "#cdd6f4"
SUBTEXT_COLOR = "#a6adc8"
ACCENT_BLUE = "#89b4fa"
ACCENT_GREEN = "#a6e3a1"
ACCENT_RED = "#f38ba8"
ACCENT_ORANGE = "#fab387"
BORDER_COLOR = "#313244"

# Select OS-native font family
CURRENT_SYSTEM = platform.system()
if CURRENT_SYSTEM == "Darwin":
    MAIN_FONT = "Helvetica Neue"
elif CURRENT_SYSTEM == "Windows":
    MAIN_FONT = "Segoe UI"
else:
    MAIN_FONT = "DejaVu Sans"

class CacheCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dev & System Cache Cleaner")
        self.root.geometry("840x700")
        self.root.minsize(750, 600)
        self.root.configure(bg=BG_COLOR)

        self.current_os = CURRENT_SYSTEM
        self.targets = []
        self.scanned_items = []
        self.check_vars = {}

        self._setup_styles()
        self._build_ui()

        # Start initial scan in background
        self.refresh_scan()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure dark theme styles with OS-native fonts
        style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR, font=(MAIN_FONT, 10))
        style.configure("TFrame", background=BG_COLOR)
        style.configure("Card.TFrame", background=CARD_BG, relief="flat", borderwidth=1)
        style.configure("Header.TFrame", background=HEADER_BG)

        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure("Sub.TLabel", background=BG_COLOR, foreground=SUBTEXT_COLOR, font=(MAIN_FONT, 9))
        style.configure("Title.TLabel", background=HEADER_BG, foreground=ACCENT_BLUE, font=(MAIN_FONT, 16, "bold"))
        style.configure("OSTag.TLabel", background=HEADER_BG, foreground=ACCENT_ORANGE, font=(MAIN_FONT, 10, "bold"))

        style.configure("Total.TLabel", background=CARD_BG, foreground=ACCENT_GREEN, font=(MAIN_FONT, 14, "bold"))

        # Button styles
        style.configure("Primary.TButton", font=(MAIN_FONT, 10, "bold"), background=ACCENT_BLUE, foreground="#11111b", borderwidth=0, padding=8)
        style.map("Primary.TButton", background=[("active", "#74c7ec")])

        style.configure("Danger.TButton", font=(MAIN_FONT, 10, "bold"), background=ACCENT_RED, foreground="#11111b", borderwidth=0, padding=8)
        style.map("Danger.TButton", background=[("active", "#f5e0dc")])

        style.configure("Secondary.TButton", font=(MAIN_FONT, 10), background=BORDER_COLOR, foreground=TEXT_COLOR, borderwidth=0, padding=8)
        style.map("Secondary.TButton", background=[("active", "#45475a")])

        # Progress bar
        style.configure("TProgressbar", thickness=8, troughcolor=CARD_BG, background=ACCENT_BLUE)

    def _build_ui(self):
        # Header Bar
        header = ttk.Frame(self.root, style="Header.TFrame", padding=15)
        header.pack(fill="x")

        os_icon = "macOS" if self.current_os == "Darwin" else ("Windows" if self.current_os == "Windows" else "Linux")
        
        lbl_title = ttk.Label(header, text="Dev & System Cache Cleaner", style="Title.TLabel")
        lbl_title.pack(side="left")

        lbl_os = ttk.Label(header, text=f"  [{os_icon}]  ", style="OSTag.TLabel")
        lbl_os.pack(side="right")

        # Main Scrollable Body
        main_container = ttk.Frame(self.root, padding=15)
        main_container.pack(fill="both", expand=True)

        # Overview Card
        overview_card = ttk.Frame(main_container, style="Card.TFrame", padding=15)
        overview_card.pack(fill="x", pady=(0, 15))

        lbl_summary_title = ttk.Label(overview_card, text="Temizlenebilir Toplam Alan:", font=(MAIN_FONT, 10), background=CARD_BG, foreground=SUBTEXT_COLOR)
        lbl_summary_title.pack(anchor="w")

        self.lbl_total_size = ttk.Label(overview_card, text="Hesaplanıyor...", style="Total.TLabel")
        self.lbl_total_size.pack(anchor="w", pady=(4, 0))

        # Targets Checklist Label
        lbl_checklist = ttk.Label(main_container, text="Temizlenecek Önbellek Türleri", font=(MAIN_FONT, 11, "bold"), foreground=ACCENT_BLUE)
        lbl_checklist.pack(anchor="w", pady=(0, 8))

        # Canvas Frame for Scrollable Checklist
        list_card = ttk.Frame(main_container, style="Card.TFrame", padding=10)
        list_card.pack(fill="both", expand=True, pady=(0, 15))

        self.canvas = tk.Canvas(list_card, bg=CARD_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_card, orient="vertical", command=self.canvas.yview)
        
        self.scroll_frame = ttk.Frame(self.canvas, style="Card.TFrame")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Progress & Status Bar
        self.progress = ttk.Progressbar(main_container, mode="determinate")
        self.progress.pack(fill="x", pady=(0, 8))

        self.lbl_status = ttk.Label(main_container, text="Hazır", style="Sub.TLabel")
        self.lbl_status.pack(anchor="w", pady=(0, 10))

        # Action Buttons Footer
        footer = ttk.Frame(main_container)
        footer.pack(fill="x")

        btn_refresh = ttk.Button(footer, text="Yeniden Tara", style="Secondary.TButton", command=self.refresh_scan)
        btn_refresh.pack(side="left", padx=(0, 10))

        btn_clean_selected = ttk.Button(footer, text="Seçilenleri Temizle", style="Primary.TButton", command=self.clean_selected)
        btn_clean_selected.pack(side="right")

        btn_clean_all = ttk.Button(footer, text="Tümünü Temizle", style="Danger.TButton", command=self.clean_all)
        btn_clean_all.pack(side="right", padx=(0, 10))

    def _get_target_list(self):
        home = Path.home()
        system = self.current_os
        targets = []

        if system == "Windows":
            local_app_data = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
            app_data = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
            temp_dir = Path(os.environ.get("TEMP", local_app_data / "Temp"))

            targets = [
                ("User Temp (%TEMP%)", temp_dir, "Geçici sistem ve uygulama dosyaları"),
                ("Gradle Cache", home / ".gradle" / "caches", "Android / Java derleme bağımlılıkları"),
                ("NPM Cache", local_app_data / "npm-cache", "Node.js paket önbelleği"),
                ("Yarn Cache", local_app_data / "Yarn" / "Cache", "Yarn paket önbelleği"),
                ("Flutter / Pub Cache", local_app_data / "Pub" / "Cache", "Flutter / Dart paket önbelleği"),
                ("Pip Cache", local_app_data / "pip" / "cache", "Python paket önbelleği"),
                ("NuGet Cache", home / ".nuget" / "packages", ".NET paket önbelleği"),
                ("VS Code Cache", app_data / "Code" / "Cache", "VS Code uygulama önbelleği"),
                ("VS Code CachedData", app_data / "Code" / "CachedData", "VS Code derlenmiş kod önbelleği"),
            ]
        elif system == "Darwin":  # macOS
            library = home / "Library"
            caches = library / "Caches"
            targets = [
                ("Xcode DerivedData", library / "Developer" / "Xcode" / "DerivedData", "Xcode geçici derleme indeksleri ve derleme çıktıları"),
                ("Xcode Archives", library / "Developer" / "Xcode" / "Archives", "Xcode derleme arşivleri"),
                ("CocoaPods Cache", caches / "CocoaPods", "iOS pod paket önbelleği"),
                ("User Caches (~/Library/Caches)", caches, "macOS uygulama önbellekleri"),
                ("Gradle Cache", home / ".gradle" / "caches", "Android derleme önbelleği"),
                ("NPM Cache", home / ".npm" / "_cacache", "Node.js npm önbelleği"),
                ("Yarn Cache", caches / "Yarn", "Yarn paket önbelleği"),
                ("Flutter / Pub Cache", home / ".pub-cache", "Flutter paket önbelleği"),
                ("Homebrew Cache", caches / "Homebrew", "Homebrew paket indirme arşivleri"),
                ("Pip Cache", caches / "pip", "Python paket önbelleği"),
            ]
        else:  # Linux
            caches = home / ".cache"
            targets = [
                ("User Cache (~/.cache)", caches, "Linux sistem önbellekleri"),
                ("Gradle Cache", home / ".gradle" / "caches", "Android derleme önbelleği"),
                ("NPM Cache", home / ".npm", "Node.js önbelleği"),
                ("Pub Cache", home / ".pub-cache", "Flutter paket önbelleği"),
                ("Pip Cache", caches / "pip", "Python paket önbelleği"),
            ]
        return targets

    def refresh_scan(self):
        self.lbl_status.config(text="Önbellekler taranıyor, lütfen bekleyin...")
        self.lbl_total_size.config(text="Hesaplanıyor...")
        self.progress.config(mode="indeterminate")
        self.progress.start(10)

        # Clear existing checklist UI
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        def scan_worker():
            targets = self._get_target_list()
            scanned = []
            total_bytes = 0

            for name, path, desc in targets:
                if path.exists():
                    size = get_folder_size(path)
                    total_bytes += size
                    scanned.append({"name": name, "path": path, "desc": desc, "size": size, "exists": True})
                else:
                    scanned.append({"name": name, "path": path, "desc": desc, "size": 0, "exists": False})

            self.root.after(0, lambda: self._update_scan_results(scanned, total_bytes))

        threading.Thread(target=scan_worker, daemon=True).start()

    def _update_scan_results(self, scanned, total_bytes):
        self.scanned_items = scanned
        self.check_vars = {}

        self.progress.stop()
        self.progress.config(mode="determinate", value=0)
        self.lbl_status.config(text="Tarama tamamlandı.")
        self.lbl_total_size.config(text=f"{format_size(total_bytes)}")

        for idx, item in enumerate(scanned):
            item_frame = tk.Frame(self.scroll_frame, bg=CARD_BG, pady=6, padx=8)
            item_frame.pack(fill="x", expand=True, pady=2)

            var = tk.BooleanVar(value=(item["exists"] and item["size"] > 0))
            self.check_vars[item["name"]] = var

            chk = tk.Checkbutton(
                item_frame, text=f" {item['name']}", variable=var,
                bg=CARD_BG, fg=TEXT_COLOR, selectcolor=BG_COLOR,
                activebackground=CARD_BG, activeforeground=ACCENT_BLUE,
                font=(MAIN_FONT, 10, "bold") if item["size"] > 0 else (MAIN_FONT, 10)
            )
            chk.pack(side="left")

            size_str = format_size(item["size"]) if item["exists"] else "Bulunamadı"
            size_color = ACCENT_GREEN if item["size"] > 0 else SUBTEXT_COLOR

            lbl_size = tk.Label(item_frame, text=size_str, bg=CARD_BG, fg=size_color, font=(MAIN_FONT, 10, "bold"))
            lbl_size.pack(side="right", padx=(10, 0))

            lbl_desc = tk.Label(item_frame, text=item["desc"], bg=CARD_BG, fg=SUBTEXT_COLOR, font=(MAIN_FONT, 9))
            lbl_desc.pack(side="right")

    def clean_selected(self):
        selected_items = [item for item in self.scanned_items if self.check_vars.get(item["name"], tk.BooleanVar()).get() and item["size"] > 0]
        
        if not selected_items:
            messagebox.showinfo("Bilgi", "Temizlemek için en az bir önbellek seçmelisiniz.")
            return

        confirm = messagebox.askyesno("Temizlik Onayı", f"Seçilen {len(selected_items)} adet önbellek klasörü temizlenecek. Devam etmek istiyor musunuz?")
        if not confirm:
            return

        self._start_cleanup(selected_items)

    def clean_all(self):
        all_cleanable = [item for item in self.scanned_items if item["exists"] and item["size"] > 0]
        if not all_cleanable:
            messagebox.showinfo("Bilgi", "Temizlenecek aktif önbellek bulunamadı.")
            return

        confirm = messagebox.askyesno("Tümünü Temizle", "TÜM önbellekler silinecek. Onaylıyor musunuz?")
        if not confirm:
            return

        self._start_cleanup(all_cleanable)

    def _start_cleanup(self, items_to_clean):
        self.progress.config(mode="determinate", value=0, maximum=len(items_to_clean))
        self.lbl_status.config(text="Temizlik başlatılıyor...")

        def cleanup_worker():
            total_freed = 0
            for idx, item in enumerate(items_to_clean):
                self.root.after(0, lambda name=item['name']: self.lbl_status.config(text=f"Temizleniyor: {name}..."))
                freed = clean_directory(item["path"])
                total_freed += freed
                self.root.after(0, lambda val=idx+1: self.progress.config(value=val))

            # Run Mac extras if on macOS
            if self.current_os == "Darwin":
                self.root.after(0, lambda: self.lbl_status.config(text="macOS iOS Simülatör ve CocoaPods temizliği yapılıyor..."))
                try:
                    subprocess.run(["xcrun", "simctl", "delete", "unavailable"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.run(["pod", "cache", "clean", "--all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass

            self.root.after(0, lambda: self._on_cleanup_finished(total_freed))

        threading.Thread(target=cleanup_worker, daemon=True).start()

    def _on_cleanup_finished(self, total_freed):
        self.lbl_status.config(text="Temizlik başarıyla tamamlandı!")
        messagebox.showinfo("Başarılı", f"Temizlik tamamlandı!\nToplanan Boş Alan: {format_size(total_freed)}")
        self.refresh_scan()

def main():
    root = tk.Tk()
    app = CacheCleanerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
