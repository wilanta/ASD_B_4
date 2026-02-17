"""
==========================================================
ID Generator
Membuat id dengan format 3 huruf acak dan 3 angka acak untuk penyimpanan data

Fungsi/fitur:
1. generateID
==========================================================
"""

# Import utilities yang dibutuhkan fungsi generateID
import random
import string

# ------------------------------
# Nama fungsi: generateID
# Penjelasan fungsi : Untuk membuat id dengan format 3 huruf acak (uppercase) dan 3 angka acak untuk penyimpanan data.
# ------------------------------
def generateID():
    # Generate 3 huruf acak (A-Z)
    huruf = ''.join(random.choices(string.ascii_uppercase, k=3))
    
    # Generate 3 angka acak (0-9)
    angka = ''.join(random.choices(string.digits, k=3))
    
    # Gabungkan huruf dan angka
    return huruf + angka

print(generateID())