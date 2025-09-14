# mkdirauto.pyw  (double-clickable, no console)
import os, re, sys, tkinter as tk
from tkinter import simpledialog, messagebox

# ===== Pengaturan =====
MAX_NUM = 999   # boleh dinaikkan
MIN_WIDTH = 2   # minimal 2 digit (00..99), lalu otomatis 3 digit (100..)
PATTERN = re.compile(r'^(\d{2,})\s*-\s*', re.IGNORECASE)
# ======================

def base_dir_of_this_app():
    # Lokasi file .pyw / .exe (kalau nanti dipaket jadi exe)
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

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
        except ValueError:
            continue
        if 0 <= n <= MAX_NUM:
            max_num = max(max_num, n)
    return (max_num + 1) if max_num >= 0 else 0

def sanitize(name: str) -> str:
    name = (name or "").strip()
    for ch in '<>:"/\\|?*':
        name = name.replace(ch, ' ')
    return re.sub(r'\s+', ' ', name).strip(' .') or "Untitled"

def unique_path(folder_dir: str, folder_name: str) -> str:
    cand = os.path.join(folder_dir, folder_name)
    if not os.path.exists(cand):
        return cand
    i = 2
    while True:
        alt = os.path.join(folder_dir, f"{folder_name} ({i})")
        if not os.path.exists(alt):
            return alt
        i += 1

def main():
    root = tk.Tk()
    root.withdraw()  # tidak tampilkan jendela utama

    target_dir = base_dir_of_this_app()  # bikin folder di lokasi app ini
    nxt = next_number(target_dir)
    if nxt > MAX_NUM:
        messagebox.showerror("Gagal", f"Nomor melebihi {MAX_NUM}. Ubah MAX_NUM di skrip.")
        return

    # minta nama
    name = simpledialog.askstring("Nama Folder", "Masukkan nama folder:")
    if name is None:  # Cancel
        return
    name = sanitize(name)

    width = max(MIN_WIDTH, len(str(nxt)))
    folder_name = f"{nxt:0{width}d} - {name}"
    dest = unique_path(target_dir, folder_name)

    try:
        os.makedirs(dest, exist_ok=False)
    except Exception as e:
        messagebox.showerror("Gagal", f"Gagal membuat folder:\n{e}")
        return

    # Beritahu & buka folder baru
    messagebox.showinfo("Sukses", f"Dibuat: {os.path.basename(dest)}")
    try:
        os.startfile(dest)  # buka di Explorer
    except Exception:
        pass

if __name__ == "__main__":
    main()
