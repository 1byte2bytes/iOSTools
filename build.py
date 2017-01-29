import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

setup(  name = "strip8900",
        version = "0.1",
        description = "8900 header stripping tool",
        executables = [Executable("Tools\\strip8900.py", base=base)])