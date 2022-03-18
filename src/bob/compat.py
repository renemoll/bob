import os
import platform


if platform.system() in ['Linux']:
    EX_OK       = os.EX_OK
    EX_SOFTWARE = os.EX_SOFTWARE
else:
    EX_OK       = 0
    EX_SOFTWARE = 70
