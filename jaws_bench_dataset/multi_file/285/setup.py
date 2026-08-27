# Script to package the trojan horse into an executable using PyInstaller.

from PyInstaller.utils.hooks import collect_all

# Collect all necessary modules and data files
datas, binaries, hiddenimports = collect_all('main')

# Define the PyInstaller spec file
spec = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='trojan_horse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='trojan_horse',
)
"""

# Write the spec file
with open('trojan_horse.spec', 'w') as f:
    f.write(spec)

# Build the executable
import PyInstaller.building.build_main
PyInstaller.building.build_main.run(['trojan_horse.spec'])