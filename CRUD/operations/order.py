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


def orderKursi(user_ticket: int, available_seats_list: list):
    "Order Kursi"

    # Menu
    print("=== Kursi Tersedia ===")
    print(available_seats_list)

    # User select seats
    selected_seats = []  # List to hold user's choice(s)
    for i in range(user_ticket):
        while True:  # Loop until a valid seat is selected
            select = input(f"\nPilih Kursi Tiket ke-{i + 1}: ").upper().strip()
            # Transfer seat from available seat list if true
            if select in available_seats_list:
                available_seats_list.remove(select)
                selected_seats.append(select)
                break
            # Print error if false
            else:
                print("Kursi tidak valid / sudah terpakai.")
    return user_ticket, selected_seats  # Return ticket amount and selected seats


# ------------------------------
# Nama fungsi: resetOrder
# Penjelasan fungsi : Untuk mereset sistem antrean menjadi 0 antrean kembali.
# ------------------------------
def resetOrder():
    pass
