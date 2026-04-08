import os
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
include_files = []
base_dir = sys.base_prefix
for dll_name in ("python314.dll", "VCRUNTIME140.dll", "VCRUNTIME140_1.dll"):
    source_path = os.path.join(base_dir, dll_name)
    if os.path.exists(source_path):
        include_files.append((source_path, dll_name))

build_exe_options = {
    "packages": ["customtkinter", "google.genai", "cryptography", "google.auth", "google.oauth2"],
    "excludes": [],
    "include_files": include_files,
}

# base="Win32GUI" should be used only for Windows GUI app
base = None

setup(
    name="Model Chat",
    version="1.0",
    description="Script management app",
    options={"build_exe": build_exe_options},
    executables=[Executable("Scritp.py", base=base)]
)