import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Console"

build_exe_options = {"packages": ['idna', 'lxml']}

setup(  name = "TimeCandy",
        version = "1.10",
        description = "Sweet Timetabling for Melbourne University.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)]
        )