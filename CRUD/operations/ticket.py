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

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


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
        new_node = Node(nama, jumlah_tiket, nomor_kursi, urutan_antrean, judul_film)

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

        console = Console()

        # Jika antrean kosong
        if self.isEmpty():
            console.print(
                Panel(
                    "[bold red]Pemesanan kosong![/bold red]",
                    title="[bold red]Daftar Pemesanan[/bold red]",
                    border_style="red",
                )
            )
            return

        table = Table(title="Daftar Pemesanan Tiket", expand=False)

        table.add_column("No", justify="center", width=5)
        table.add_column("Nama", width=20)
        table.add_column("Jumlah Tiket", justify="center", width=15)
        table.add_column("Tanggal", width=20)

        current = self.head
        i = 1

        while current:
            table.add_row(
                str(i), current.nama, str(current.jumlah_tiket), str(current.create_at)
            )
            current = current.next
            i += 1

        console.print(table)

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
            jumlah_tiket (int): Jumlah tiket yang dibatalkan
            nomor_kursi (list): Nomor kursi yang dibatalkan
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

        return None, None

    # ------------------------------
    # Nama fungsi: searchTicket
    # Penjelasan fungsi : Untuk satu mencari ticket dalam linked list.
    # ------------------------------
    def searchTicket(self, nama):
        """
        Mencari data pemesanan.

        Args:
            nama (str): Nama customer

        Returns:
            found (bool): Tampilkan list atau tidak
        """

        current = self.head
        found = False
        console = Console()

        while current:
            if current.nama.lower() == nama.lower():
                detail_table = Table(
                    show_header=False, expand=False, box=None, padding=(0, 1)
                )

                detail_table.add_column("Field", style="cyan", width=15)
                detail_table.add_column("Value", style="white")

                detail_table.add_row("Nama", current.nama)
                detail_table.add_row("Jumlah Tiket", str(current.jumlah_tiket))
                detail_table.add_row(
                    "Nomor Kursi", ", ".join(seat_sort(current.nomor_kursi))
                )
                detail_table.add_row("Judul Film", current.judul_film)
                detail_table.add_row("Tanggal", str(current.create_at))

                console.print(
                    Panel(detail_table, title="Detail Pemesanan", border_style="green")
                )

                found = True

            current = current.next

        return found
