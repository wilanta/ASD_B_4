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

# ------------------------------
# Nama fungsi: orderKursi
# Penjelasan fungsi : Untuk memilihkan kursi kosong untuk customer secara bebas.
# ------------------------------


def orderKursi(available_seats_list: list):  # kursi_id PLACEHOLDER
    "Order Kursi"
    max_kursi_per_cust = 4  # Constant

    # Loop user input
    while True:
        # Input validation (must be int)
        try:
            user_ticket = int(input("Masukkan jumlah tiket yang dipesan: "))
            # If not between 1-4
            if user_ticket > max_kursi_per_cust or user_ticket < 0:
                print("Hanya bisa 1-4 tiket!")
            # Else if over the quota
            elif user_ticket > len(available_seats_list):
                print(
                    f"Hanya tersisa {len(available_seats_list)} kuota!")
        except ValueError:
            print("Masukkan bilangan yang valid!")
        break  # exit loop

    # Menu
    print("=== Kursi Tersedia ===")
    print(available_seats_list)
    # User select seats
    for i in range(user_ticket):
        select = input(f"Pilih Kursi Tiket ke-{i+1}: ").upper().strip()
        selected_seats = []  # List to hold user's choice(s)
        # Transfer seat from available seat list if true
        # Print error if false
        if select in available_seats_list:
            available_seats_list.remove(select)
            selected_seats.append(select)
        else:
            print("Kursi tidak valid / sudah terpakai.")
    return user_ticket, selected_seats  # Return ticket amount and selected seats

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
