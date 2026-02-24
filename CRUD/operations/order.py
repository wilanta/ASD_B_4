"""
==========================================================
Manajemen Pemesanan Kursi & Manajemen Pemesanan Tiket
Untuk memilih kursi yang kosong untuk customer secara bebas
dan menyimpan pemesanan ke log_antrean.txt.

Kontributor : Fateeh Falah Hendarto
Fungsi/fitur:
1. orderKursi
2. storeOrder
3. resetOrder
==========================================================
"""

# Dependencies
from rich import print

# Utils
from CRUD.utils.dataOps import getAllData

# ------------------------------
# Nama fungsi: orderKursi
# Penjelasan fungsi : Untuk memilihkan kursi kosong untuk customer secara bebas.
# ------------------------------


def orderKursi(kursi_id='ABC123'):  # kursi_id PLACEHOLDER
    "Order Kursi"
    data = getAllData('data_film')  # Fetch
    max_kursi_per_cust = 4  # Constant

    # Menu
    print("=== Kursi Tersedia ===")
    available_seats = [
        "K" + str(i) for i in range(1, int(data[kursi_id]['kuota_penonton']))]
    print(available_seats)

    # Loop user input
    while True:
        try:
            user_ticket = int(input("Masukkan jumlah tiket yang dipesan: "))
            # If not between 1-4
            if user_ticket > max_kursi_per_cust or user_ticket < 0:
                print("Hanya bisa 1-4 tiket!")
            # Else if over the quota
            elif user_ticket > int(data[kursi_id]['kuota_penonton']):
                print(
                    f"Hanya tersisa {data[kursi_id]['kuota_penonton']} kuota!")
        # If not int
        except ValueError:
            print("Masukkan bilangan yang valid!")
        break  # exit loop

    # User select seats
    for _ in range(user_ticket):
        select = input("Pilih Kursi: ").upper().strip()
        selected_seats = []  # List to hold user's choice(s)
        # Transfer seat from available seat list if true
        # Print error if false
        if select in available_seats:
            available_seats.remove(select)
            selected_seats.append(select)
        else:
            print("Kursi tidak valid / sudah terpakai.")
    return user_ticket, selected_seats  # Return ticket amount and selected seats


orderKursi()

# ------------------------------
# Nama fungsi: storeOrder
# Penjelasan fungsi : Untuk menyimpan pemesanan customer yang telah dilayani dan memilih kursi
# ke log_pemesanan.txt dengan format log_id,nama,jumlah_ticket,urutan_antrean,judul.
# ------------------------------


def storeOrder():
    pass

# ------------------------------
# Nama fungsi: resetOrder
# Penjelasan fungsi : Untuk mereset sistem antrean menjadi 0 antrean kembali.
# ------------------------------


def resetOrder():
    pass
