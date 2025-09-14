# interface.py — UI Components untuk mkdirauto
import os, tkinter as tk
from tkinter import ttk, messagebox, filedialog

try:
    from PIL import Image, ImageTk
except Exception:
    messagebox.showerror("Auto Numbered Folder",
        "Fitur preview icon membutuhkan Pillow.\n\nJalankan:\n  pip install pillow")
    import sys
    sys.exit(1)

# -------- Icon Picker --------
class IconPicker(tk.Toplevel):
    def __init__(self, parent, start_dir, icons_dir):
        super().__init__(parent)
        self.title("Choose folder icon")
        self.configure(bg="#1e1f22")
        self.selected = None
        self.icons_dir = icons_dir
        self.start_dir = start_dir if os.path.isdir(start_dir) else icons_dir
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
    def __init__(self, app_title, default_icon, icons_dir, target_dir, next_number_func, sanitize_func, unique_path_func, set_folder_icon_func):
        super().__init__()
        self.title(app_title)
        self.app_title = app_title
        self.default_icon = default_icon
        self.icons_dir = icons_dir
        self.target_dir = target_dir
        self.next_number_func = next_number_func
        self.sanitize_func = sanitize_func
        self.unique_path_func = unique_path_func
        self.set_folder_icon_func = set_folder_icon_func
        
        self.icon_path = default_icon  # default
        self.nxt = next_number_func(target_dir)
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
        ttk.Label(wrap, text=f"Next number: {self.nxt:0{max(2, len(str(self.nxt)))}d}", style="Muted.TLabel").grid(row=2, column=0, columnspan=3, sticky="w", pady=(0, pad))

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
        dlg = IconPicker(self, self.icons_dir, self.icons_dir)
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
            messagebox.showwarning(self.app_title, "Nama folder tidak boleh kosong.")
            return
        name = self.sanitize_func(raw)
        nxt = self.nxt
        if nxt > 999:  # MAX_NUM
            messagebox.showerror(self.app_title, f"Nomor melebihi 999.")
            return
        width = max(2, len(str(nxt)))  # MIN_WIDTH
        folder_name = f"{nxt:0{width}d} - {name}"
        dest = self.unique_path_func(self.target_dir, folder_name)

        try:
            os.makedirs(dest, exist_ok=False)
        except Exception as e:
            messagebox.showerror(self.app_title, f"Gagal membuat folder:\n{e}")
            return

        icon_to_use = self.icon_path if os.path.isfile(self.icon_path) else self.default_icon
        try:
            self.set_folder_icon_func(dest, icon_to_use)
        except Exception as e:
            messagebox.showwarning(self.app_title, f"Folder dibuat, tapi gagal set icon:\n{e}")

        try: os.startfile(dest)
        except Exception: pass

        messagebox.showinfo(self.app_title, f"Dibuat: {os.path.basename(dest)}")
        self.destroy()