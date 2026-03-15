"""
==========================================================
Manajemen Data Pemesanan (Linked List)
Berisi algoritma Linked List untuk mengelola dan menyimpan data pemesanan tiket.

Kontributor : Fateeh Falah Hendarto
Fungsi/fitur:
1. addTicket
2. showTickets
3. deleteTicket
4. searchTicket
==========================================================
"""

from CRUD.utils.node import Node
from CRUD.utils.seatSort import seat_sort


# ````````````````````````````````````````````
# Nama kelas: Ticket
# Penjelasan kelas : Untuk membuat linked list yang akan digunakan untuk
# menyimpan data dan log pemesanan tiket.
# ````````````````````````````````````````````
class Ticket:
    "LinkedList untuk data pemesanan."

    def __init__(self):
        self.head = None
        self.tail = None

    # ------------------------------
    # Nama fungsi: addTicket
    # Penjelasan fungsi : Untuk menambahkan ticket ke linked list.
    # ------------------------------
    def addTicket(self, nama, jumlah_tiket, nomor_kursi, urutan_antrean, judul_film):
        """
        Menambah tiket ke data.

        Args:
            nama (str) : Nama customer
            jumlah_tiket (int) : Jumlah tiket yang dipesan
            nomor_kursi (list) : List kursi yang dipilih
            urutan_antrean (int) : Urutan dalam antrean
            nama (str) : Nama customer
        """

        # Membuat node baru
        new_node = Node(nama, jumlah_tiket, nomor_kursi,
                        urutan_antrean, judul_film)

        # Jika list kosong, buatkan head & tail dengan node baru
        if self.isEmpty():
            self.head = self.tail = new_node
            return

        # Buat link baru, lalu masukkan node baru ke posisi terakhir
        self.tail.next = new_node
        self.tail = new_node

    # ------------------------------
    # Nama fungsi: isEmpty
    # Penjelasan fungsi : Untuk mengecek apakah linked list kosong atau tidak.
    # ------------------------------
    def isEmpty(self):
        "Cek apabila Linked List kosong."
        return self.head is None

    # ------------------------------
    # Nama fungsi: showTickets
    # Penjelasan fungsi : Untuk menampilkan semua ticket yang berada dalam linked list.
    # ------------------------------
    def showTickets(self):
        "Menunjukkan daftar pemesanan tiket."
        current = self.head  # Inisialisasi awal node sebelum looping
        i = 1  # Index urutan
        print("=" * 60)
        print("No", end=" | ")
        print("Nama", end=f"{' ' * 12}| ")
        print("Jumlah Tiket", end=" | ")
        print("Tanggal")
        print("=" * 60)
        # Print jika list kosong
        if self.isEmpty():
            print("Data tidak dapat ditemukan.")
        # Looping isi list
        while current:
            print(
                f"{i: <2} | {current.nama: <15} | {current.jumlah_tiket: <12} | {current.create_at}")
            current = current.next
            i += 1

    # ------------------------------
    # Nama fungsi: deleteTicket
    # Penjelasan fungsi : Untuk menghapus satu ticket dalam linked list.
    # ------------------------------

    def deleteTicket(self, nama):
        """
        Menghapus tiket dari data.

        Args:
            nama (str): Nama customer

        Return:
            1. Jumlah tiket yang dibatalkan
            2. Nomor kursi yang dibatalkan
        """
        current = self.head  # Variabel sementara dari awal node

        # Jika nama ditemukan di awal node, hapuskan dan return jumlah tiket customer
        if current and current.nama == nama:
            self.head = current.next
            return current.jumlah_tiket, current.nomor_kursi

        # Traverse dari awal hingga ketemu nama
        prev = None
        while current and current.nama != nama:
            prev = current
            current = current.next

        # Apabila namanya ditemukan, hapus dan return jumlah tiket customer
        # Else, print error dan return 0
        if current:
            prev.next = current.next
            return current.jumlah_tiket, current.nomor_kursi

        print("Nama tidak ditemukan!")
        return 0

    # ------------------------------
    # Nama fungsi: searchTicket
    # Penjelasan fungsi : Untuk satu mencari ticket dalam linked list.
    # ------------------------------
    def searchTicket(self, nama):
        """
        Mencari data pemesanan.

        Args:
            nama (str): Nama customer
        """

        current = self.head  # Iterasi dari awal
        found = False  # Flag untuk mengecek keberadaan data
        while current:
            if current.nama == nama:
                print("=" * 45)
                print("Nama\t\t:", current.nama)
                print("Jumlah Tiket\t:", current.jumlah_tiket)
                print("Nomor Kursi\t:", ', '.join(
                    seat_sort(current.nomor_kursi)))
                print("Judul Film\t:", current.judul_film)
                print("Tanggal\t\t:", current.create_at)
                print("=" * 45, '\n')
                found = True
            current = current.next

        if not found:  # Jika nama tidak ditemukan
            print("Nama tidak ditemukan.")
