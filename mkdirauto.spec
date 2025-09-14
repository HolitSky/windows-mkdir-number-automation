# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mkdirauto.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        ('icons', 'icons'),
        ('defaulticons', 'defaulticons'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='mkdirauto',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='defaulticons\\defaultapp.ico',
)

# Manual copy of defaulticons folder
import shutil
import os
if os.path.exists('defaulticons'):
    shutil.copytree('defaulticons', 'dist/defaulticons', dirs_exist_ok=True)
