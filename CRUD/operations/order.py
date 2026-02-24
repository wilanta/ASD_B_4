"""
==========================================================
Manajemen Pemesanan Kursi & Manajemen Pemesanan Tiket
Untuk memilih kursi yang kosong untuk customer secara bebas dan menyimpan pemesanan ke log_antrean.txt.

Kontributor : Fateeh Falah Hendarto
Fungsi/fitur:
1. orderKursi
2. storeOrder
3. resetOrder
==========================================================
"""

# Dependencies
from rich import print

# ------------------------------
# Nama fungsi: orderKursi
# Penjelasan fungsi : Untuk memilihkan kursi kosong untuk customer secara bebas.
# ------------------------------
def orderKursi():
    with open('../data/data_film.txt', 'r', encoding='utf-8') as file:
        # Loop setiap baris di file
        for row in file:
            row = row.strip()
            _id_film, _nama_film, kuota_film = row.split(',')
    print(kuota_film)
    max_kursi_per_cust = 4
    while True:
        try:
            user_ticket = int(input("Masukkan jumlah tiket yang dipesan: "))
            if user_ticket > max_kursi_per_cust or user_ticket < 0:
                print("Hanya bisa 1-4 tiket!")
            elif user_ticket > kuota_film:
                print(f"Hanya tersisa {kuota_film} kuota!")
        except ValueError:
            print("Masukkan bilangan yang valid!")
    # print("=== Pilih Kursi ===")
orderKursi()
# ------------------------------
# Nama fungsi: storeOrder
# Penjelasan fungsi : Untuk menyimpan pemesanan customer yang telah dilayani dan memilih kursi ke log_pemesanan.txt dengan format log_id,nama,jumlah_ticket,urutan_antrean,judul.
# ------------------------------
def storeOrder():
    pass

# ------------------------------
# Nama fungsi: resetOrder
# Penjelasan fungsi : Untuk mereset sistem antrean menjadi 0 antrean kembali.
# ------------------------------
def resetOrder():
    pass