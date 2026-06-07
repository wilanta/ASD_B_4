"""
==========================================================
Clear Screen
Membersihkan layar terminal secara cross-platform (Windows & Unix)

Fungsi/fitur:
1. _clear
==========================================================
"""

import os
import sys


# ------------------------------
# Nama fungsi: _clear
# Penjelasan fungsi : Membersihkan seluruh isi layar terminal.
# Digunakan untuk menampilkan ulang menu dan memperbarui tampilan layar.
# ------------------------------
def _clear():
    # cls untuk Windows, clear untuk Unix/Linux/macOS
    os.system("cls" if sys.platform == "win32" else "clear")
