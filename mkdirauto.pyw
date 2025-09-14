# mkdirauto.pyw — GUI modern + icon picker (recursive)
import os, re, sys, subprocess, tkinter as tk
from tkinter import ttk, messagebox, filedialog

try:
    from PIL import Image, ImageTk
except Exception:
    messagebox.showerror("Auto Numbered Folder",
        "Fitur preview icon membutuhkan Pillow.\n\nJalankan:\n  pip install pillow")
    sys.exit(1)

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

# -------- Icon Picker --------
class IconPicker(tk.Toplevel):
    def __init__(self, parent, start_dir):
        super().__init__(parent)
        self.title("Choose folder icon")
        self.configure(bg="#1e1f22")
        self.selected = None
        self.start_dir = start_dir if os.path.isdir(start_dir) else ICONS_DIR
        self._photos = []   # keep refs
        self._build_ui()
        self._load_icons(self.start_dir)
        self.grab_set()
        self.transient(parent)
        self._center(820, 540)

    def _build_ui(self):
        style = ttk.Style(self)
        try: style.theme_use("clam")
        except: pass
        style.configure(".", background="#1e1f22", foreground="#e8e8e8")
        style.configure("Muted.TLabel", foreground="#9aa0a6")

        wrap = ttk.Frame(self, padding=12)
        wrap.pack(fill="both", expand=True)

        top = ttk.Frame(wrap)
        top.pack(fill="x")
        ttk.Label(top, text="Icons folder:", style="Muted.TLabel").pack(side="left")
        self.path_var = tk.StringVar(value=self.start_dir)
        ttk.Entry(top, textvariable=self.path_var).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(top, text="Browse…", command=self._browse).pack(side="left")

        self.preview = ttk.Label(wrap, text="Preview: (none)", style="Muted.TLabel")
        self.preview.pack(anchor="w", pady=(8,6))

        # scrollable grid
        self.canvas = tk.Canvas(wrap, bg="#1e1f22", highlightthickness=0)
        vs = ttk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vs.set)
        vs.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.grid_frame = ttk.Frame(self.canvas)
        self.win = self.canvas.create_window(0, 0, anchor="nw", window=self.grid_frame)
        self.grid_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._fit_width)

        btns = ttk.Frame(wrap)
        btns.pack(fill="x", pady=(10,0))
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side="right", padx=6)
        self.btn_select = ttk.Button(btns, text="Select", command=self._select, state="disabled")
        self.btn_select.pack(side="right")

    def _fit_width(self, e):
        self.canvas.itemconfigure(self.win, width=e.width)

    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _browse(self):
        d = filedialog.askdirectory(initialdir=self.start_dir, title="Pick icons folder")
        if d:
            self.path_var.set(d)
            self._load_icons(d)

    def _load_icons(self, root):
        for w in self.grid_frame.winfo_children(): w.destroy()
        self._photos.clear()
        paths = []
        for r, _, files in os.walk(root):
            for f in files:
                if f.lower().endswith(".ico"):
                    paths.append(os.path.join(r, f))
        paths.sort()

        if not paths:
            ttk.Label(self.grid_frame, text="No .ico files found.", style="Muted.TLabel").grid(sticky="w", padx=6, pady=6)
            self.selected = None
            self.btn_select.config(state="disabled")
            self.preview.configure(text="Preview: (none)", image="")
            return

        cols, size = 7, 48
        for i, p in enumerate(paths):
            try:
                im = Image.open(p).resize((size, size), Image.LANCZOS)
                ph = ImageTk.PhotoImage(im)
            except Exception:
                continue
            self._photos.append(ph)
            b = ttk.Button(self.grid_frame, image=ph, text=os.path.basename(p),
                           compound="top", command=lambda path=p: self._choose(path))
            b.grid(row=i//cols, column=i%cols, padx=8, pady=8, sticky="n")
            b.bind("<Double-Button-1>", lambda e, path=p: (self._choose(path), self._select()))

    def _choose(self, path):
        self.selected = path
        self.btn_select.config(state="normal")
        try:
            im = Image.open(path).resize((64, 64), Image.LANCZOS)
            ph = ImageTk.PhotoImage(im)
            self.preview.configure(text=f"Preview: {os.path.basename(path)}", image=ph, compound="left")
            self.preview.image = ph
        except Exception:
            self.preview.configure(text=f"Preview: {os.path.basename(path)}", image="")

    def _select(self):
        if self.selected:
            self.destroy()

# -------- Main App --------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.icon_path = DEFAULT_ICON  # default
        self.target_dir = BASE_DIR
        self.nxt = next_number(self.target_dir)
        self._setup_style()
        self._build()
        self._center(460, 230)

    def _setup_style(self):
        self.resizable(False, False)
        style = ttk.Style(self)
        try: style.theme_use("clam")
        except: pass
        self['bg'] = "#1e1f22"
        style.configure(".", background="#1e1f22", foreground="#e8e8e8")
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Muted.TLabel", foreground="#9aa0a6")
        style.configure("TEntry", foreground="#000000", fieldbackground="#ffffff")

    def _build(self):
        pad = 12
        wrap = ttk.Frame(self, padding=pad); wrap.grid(row=0, column=0)

        ttk.Label(wrap, text="Create numbered folder", style="Header.TLabel").grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(wrap, text=f"Target: {self.target_dir}", style="Muted.TLabel").grid(row=1, column=0, columnspan=3, sticky="w")
        ttk.Label(wrap, text=f"Next number: {self.nxt:0{max(MIN_WIDTH, len(str(self.nxt)))}d}", style="Muted.TLabel").grid(row=2, column=0, columnspan=3, sticky="w", pady=(0, pad))

        ttk.Label(wrap, text="Folder name").grid(row=3, column=0, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(wrap, textvariable=self.name_var, width=42).grid(row=3, column=1, columnspan=2, sticky="ew")

        ttk.Label(wrap, text="Icon").grid(row=4, column=0, sticky="w", pady=(pad//2,0))
        self.icon_preview = ttk.Label(wrap, text="Default", style="Muted.TLabel")
        self.icon_preview.grid(row=4, column=1, sticky="w", pady=(pad//2,0))
        ttk.Button(wrap, text="Choose…", command=self._choose_icon).grid(row=4, column=2, sticky="e", pady=(pad//2,0))

        btns = ttk.Frame(wrap); btns.grid(row=5, column=0, columnspan=3, pady=(pad,0), sticky="e")
        ttk.Button(btns, text="Cancel", command=self.destroy).grid(row=0, column=0, padx=(0,6))
        ttk.Button(btns, text="Create", command=self._create).grid(row=0, column=1)

        self.bind("<Return>", lambda e: self._create())
        self.bind("<Escape>", lambda e: self.destroy())

    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _choose_icon(self):
        dlg = IconPicker(self, ICONS_DIR)
        self.wait_window(dlg)
        if dlg.selected:
            self.icon_path = dlg.selected
            # update small preview text/icon
            try:
                im = Image.open(self.icon_path).resize((20,20), Image.LANCZOS)
                ph = ImageTk.PhotoImage(im)
                self.icon_preview.configure(text=os.path.basename(self.icon_path), image=ph, compound="left")
                self.icon_preview.image = ph
            except Exception:
                self.icon_preview.configure(text=os.path.basename(self.icon_path), image="")

    def _create(self):
        raw = self.name_var.get().strip()
        if not raw:
            messagebox.showwarning(APP_TITLE, "Nama folder tidak boleh kosong.")
            return
        name = sanitize(raw)
        nxt = self.nxt
        if nxt > MAX_NUM:
            messagebox.showerror(APP_TITLE, f"Nomor melebihi {MAX_NUM}.")
            return
        width = max(MIN_WIDTH, len(str(nxt)))
        folder_name = f"{nxt:0{width}d} - {name}"
        dest = unique_path(self.target_dir, folder_name)

        try:
            os.makedirs(dest, exist_ok=False)
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Gagal membuat folder:\n{e}")
            return

        icon_to_use = self.icon_path if os.path.isfile(self.icon_path) else DEFAULT_ICON
        try:
            set_folder_icon(dest, icon_to_use)
        except Exception as e:
            messagebox.showwarning(APP_TITLE, f"Folder dibuat, tapi gagal set icon:\n{e}")

        try: os.startfile(dest)
        except Exception: pass

        messagebox.showinfo(APP_TITLE, f"Dibuat: {os.path.basename(dest)}")
        self.destroy()

def main():
    os.makedirs(ICONS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DEFAULT_ICON), exist_ok=True)
    app = App()
    app.mainloop()

if __name__ == "__main__":
    import re  # needed for sanitize
    main()
