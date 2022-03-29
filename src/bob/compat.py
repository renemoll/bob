"""Thin OS compatability helper."""
import os
import platform


if platform.system() in ["Linux"]:
    EX_OK = os.EX_OK
    EX_DATAERR = os.EX_DATAERR
    EX_SOFTWARE = os.EX_SOFTWARE
else:
    EX_OK = 0
    EX_DATAERR = 65
    EX_SOFTWARE = 70
