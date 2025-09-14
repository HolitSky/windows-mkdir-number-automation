# 📁 AutoMkdir - Automated Folder Creator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-Personal%20Use-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

*Aplikasi Python sederhana untuk mempercepat pembuatan folder dengan sistem penomoran otomatis*

</div>

## 🚀 Tentang Proyek

**AutoMkdir** adalah aplikasi desktop berbasis Python yang dirancang khusus untuk mempermudah dan mempercepat proses pembuatan folder dengan sistem penomoran otomatis. Aplikasi ini sangat berguna untuk mengorganisir proyek, dokumen, atau file dengan struktur yang teratur dan konsisten.

## ✨ Fitur Utama

- 🔢 **Penomoran Otomatis**: Sistem penomoran yang cerdas dan berurutan
- 🎯 **Interface Sederhana**: GUI yang user-friendly menggunakan Tkinter
- 📝 **Sanitasi Nama**: Otomatis membersihkan karakter ilegal dari nama folder
- 🔄 **Deteksi Duplikat**: Mencegah konflik nama dengan sistem penomoran tambahan
- 📂 **Auto-Open**: Langsung membuka folder yang baru dibuat di Explorer
- ⚙️ **Konfigurasi Fleksibel**: Mudah disesuaikan melalui pengaturan di kode

## 🛠️ Cara Kerja

1. **Deteksi Nomor Terakhir**: Aplikasi memindai folder yang ada dan mendeteksi nomor tertinggi
2. **Input Nama**: User memasukkan nama folder melalui dialog box
3. **Format Otomatis**: Nama diformat dengan pola `XX - Nama Folder`
4. **Validasi**: Sistem memastikan tidak ada konflik nama
5. **Pembuatan**: Folder dibuat dan langsung dibuka di Explorer

## 📋 Persyaratan Sistem

- Python 3.x
- Tkinter (biasanya sudah termasuk dalam instalasi Python)
- Windows OS (untuk fungsi `os.startfile()`)

## 🎮 Cara Penggunaan

### Menjalankan Aplikasi
```bash
# Jalankan langsung dengan double-click pada file
mkdirauto.pyw

# Atau melalui command line
python mkdirauto.pyw
```

### Langkah-langkah
1. Double-click file `mkdirauto.pyw`
2. Masukkan nama folder yang diinginkan
3. Klik OK
4. Folder akan dibuat dengan format `XX - Nama Folder`
5. Explorer akan terbuka menampilkan folder baru

## ⚙️ Konfigurasi

Anda dapat menyesuaikan pengaturan di bagian atas file:

```python
# ===== Pengaturan =====
MAX_NUM = 999   # Nomor maksimum (bisa dinaikkan)
MIN_WIDTH = 2   # Minimal 2 digit (00..99), lalu otomatis 3 digit (100..)
PATTERN = re.compile(r'^(\d{2,})\s*-\s*', re.IGNORECASE)
# ======================
```

## 📁 Struktur Proyek

```
automkdir/
├── mkdirauto.pyw          # File utama aplikasi
├── mkdirauto.spec         # Spesifikasi PyInstaller
├── README.md              # Dokumentasi proyek
├── build/                 # Folder build PyInstaller
├── dist/                  # Folder distribusi (executable)
├── icons/                 # Koleksi ikon untuk folder
└── defaulticons/          # Ikon default
```

## 🔧 Build ke Executable

Untuk membuat file executable:

```bash
# Install PyInstaller jika belum ada
pip install pyinstaller

# Build executable
pyinstaller mkdirauto.spec
```

File executable akan tersedia di folder `dist/`.

### 🎨 Custom Icon Executable

Aplikasi ini menggunakan custom icon untuk executable yang dikonfigurasi di `mkdirauto.spec`:

```python
# Di mkdirauto.spec baris 41
icon='defaulticons\\defaultapp.ico',
```

**Icon yang digunakan:**
- `defaultapp.ico` → Icon untuk file executable mkdirauto.exe
- `defaultfolder.ico` → Icon default untuk folder yang dibuat aplikasi

### 🔄 Troubleshooting Icon

Jika icon executable tidak berubah setelah build:

```powershell
# Clear Windows icon cache
Remove-Item -Force "$env:localappdata\IconCache.db"

# Restart explorer untuk refresh
taskkill /f /im explorer.exe
Start-Process explorer.exe
```

### 📦 Update & Clean Build

Setiap kali melakukan update aplikasi, lakukan clean build:

```powershell
# 1. Hapus folder build dan dist
Remove-Item -Recurse -Force build, dist

# 2. Build ulang aplikasi
pyinstaller mkdirauto.spec

# 3. Jika icon tidak berubah, clear cache
Remove-Item -Force "$env:localappdata\IconCache.db"
```

### 🚀 Menjalankan Executable

Setelah build selesai:

```powershell
# Jalankan dari command line
.\dist\mkdirauto.exe

# Atau double-click file mkdirauto.exe di folder dist/
```

**Lokasi file:** `dist/mkdirauto.exe`

## 💡 Contoh Output

Jika Anda memasukkan nama "Project Baru", aplikasi akan membuat folder:
- `00 - Project Baru` (jika belum ada folder bernomor)
- `01 - Project Baru` (jika sudah ada folder `00`)
- `02 - Project Baru` (jika sudah ada folder `00` dan `01`)

## 🎨 Kustomisasi

- **Ubah Pola Penomoran**: Modifikasi variabel `PATTERN`
- **Atur Lebar Digit**: Sesuaikan `MIN_WIDTH`
- **Batasi Nomor Maksimum**: Ubah `MAX_NUM`
- **Tambah Validasi**: Extend fungsi `sanitize()`

## 📝 Catatan Pengembangan

Proyek ini dibuat untuk kebutuhan personal dalam mengorganisir folder dengan sistem yang konsisten dan efisien. Aplikasi ini sangat cocok untuk:

- Mengorganisir proyek-proyek
- Menyusun dokumentasi berurutan
- Membuat struktur folder yang teratur
- Mempercepat workflow harian

## 🎨 Lisensi Ikon & Asset

⚠️ **PENTING - Penggunaan Asset Ikon**

Ikon-ikon yang tersedia dalam folder `icons/` dan `defaulticons/` diambil dari [Wallpapers Clan](https://wallpapers-clan.com/) dan tunduk pada ketentuan berikut:

> **⚠️ PERINGATAN LISENSI:**
> 
> *These icons and wallpapers are for personal use only.*
> *By downloading this product you agree to not share, sell or redistribute this product in any form.*

### 📋 Ketentuan Penggunaan Asset:

- ✅ **Diizinkan**: Penggunaan personal/pribadi
- ❌ **Tidak Diizinkan**: 
  - Penggunaan komersial
  - Menjual atau mendistribusikan ulang
  - Membagikan asset secara terpisah
  - Menggunakan untuk proyek komersial

### 🛡️ Disclaimer

- Semua ikon dan wallpaper adalah karya transformatif fan art
- Dimaksudkan untuk penggunaan personal dan non-komersial
- Semua trademark dan karakter adalah milik pemilik masing-masing
- Proyek ini tidak berafiliasi dengan brand manapun

**Gunakan asset ini dengan bijak dan hormati hak cipta pemilik asli!**

## 🤝 Kontribusi

Karena ini adalah proyek personal, kontribusi tidak diperlukan. Namun, Anda bebas untuk:
- Fork proyek ini
- Modifikasi sesuai kebutuhan
- Menggunakan sebagai referensi
- **Catatan**: Jika Anda fork proyek ini, pastikan untuk menghapus folder `icons/` atau ganti dengan asset yang Anda miliki lisensinya

---

<div align="center">

**Dibuat dengan ❤️ oleh [Holit Sky](https://khalidsaifullah.me/)  untuk mempermudah workflow harian**

*Happy Organizing! 📁✨*

</div>