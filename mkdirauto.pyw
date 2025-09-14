# mkdirauto.pyw — GUI modern + icon picker (recursive)
import os, re, sys, subprocess
from interface import App

# ===== Pengaturan =====
MAX_NUM = 999
MIN_WIDTH = 2
PATTERN = re.compile(r'^(\d{2,})\s*-\s*', re.IGNORECASE)
APP_TITLE = "Auto Numbered Folder"
# ======================

def app_dir():
    return os.path.dirname(sys.executable) if getattr(sys, "frozen", False) \
           else os.path.dirname(os.path.abspath(__file__))

BASE_DIR = app_dir()
ICONS_DIR = os.path.join(BASE_DIR, "icons")
DEFAULT_ICON = os.path.join(BASE_DIR, "defaulticons", "defaultfolder.ico")

def next_number(path: str) -> int:
    max_num = -1
    for name in os.listdir(path):
        full = os.path.join(path, name)
        if not os.path.isdir(full): 
            continue
        m = PATTERN.match(name)
        if not m: 
            continue
        try:
            n = int(m.group(1))
            if 0 <= n <= MAX_NUM:
                max_num = max(max_num, n)
        except ValueError:
            pass
    return (max_num + 1) if max_num >= 0 else 0

def sanitize(name: str) -> str:
    name = (name or "").strip()
    for ch in '<>:"/\\|?*':
        name = name.replace(ch, " ")
    return re.sub(r"\s+", " ", name).strip(" .") or "Untitled"

def unique_path(parent: str, name: str) -> str:
    p = os.path.join(parent, name)
    if not os.path.exists(p):
        return p
    i = 2
    while True:
        q = os.path.join(parent, f"{name} ({i})")
        if not os.path.exists(q):
            return q
        i += 1

def set_folder_icon(folder: str, icon_path: str):
    icon_path = os.path.abspath(icon_path)
    ini = os.path.join(folder, "desktop.ini")
    with open(ini, "w", encoding="utf-8") as f:
        f.write("[.ShellClassInfo]\n")
        f.write(f"IconFile={icon_path}\n")
        f.write("IconIndex=0\n")
    # desktop.ini -> Hidden+System ; folder -> System
    subprocess.run(f'attrib +h +s "{ini}"', shell=True)
    subprocess.run(f'attrib +s "{folder}"', shell=True)



def main():
    os.makedirs(ICONS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DEFAULT_ICON), exist_ok=True)
    app = App(APP_TITLE, DEFAULT_ICON, ICONS_DIR, BASE_DIR, next_number, sanitize, unique_path, set_folder_icon)
    app.mainloop()

if __name__ == "__main__":
    import re  # needed for sanitize
    main()
