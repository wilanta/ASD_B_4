"""
==========================================================
Manajemen Data Pemesanan (Linked List)
Berisi algoritma linked list untuk menyimpan dan mengelola
data pemesanan tiket bioskop secara terstruktur.

Kontributor : Fateeh Falah Hendarto

Class:
1. Ticket

Method:
1. addTicket     - Menambahkan record pemesanan ke linked list
2. showTickets   - Menampilkan seluruh daftar pemesanan
3. deleteTicket  - Menghapus satu record pemesanan berdasarkan nama
4. searchTicket  - Mencari record pemesanan berdasarkan nama
==========================================================
"""

from CRUD.utils.node import Node
from CRUD.utils.seatSort import seat_sort

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


# ````````````````````````````````````````````
# Nama kelas: Ticket
# Penjelasan kelas : Linked list untuk menyimpan data dan log pemesanan tiket.
# ````````````````````````````````````````````
class Ticket:
    """Linked list untuk data pemesanan tiket bioskop."""

    def __init__(self):
        self.head = None  # Pointer ke node pertama linked list
        self.tail = None  # Pointer ke node terakhir linked list

    # ------------------------------
    # Nama fungsi: addTicket
    # Penjelasan fungsi : Menambahkan record pemesanan baru
    # ke akhir linked list.
    # ------------------------------
    def addTicket(
        self, nama, jumlah_tiket, nomor_kursi, urutan_antrean, judul_film, customer_id
    ):
        """
        Menambahkan record pemesanan ke linked list.

        Args:
            nama (str): Nama customer.
            jumlah_tiket (int): Jumlah tiket yang dipesan.
            nomor_kursi (list): List nomor kursi yang dipilih.
            urutan_antrean (int): Urutan dalam antrean.
            judul_film (str): Judul film yang ditonton.
        """

        # Membuat node baru
        new_node = Node(
            nama=nama,
            jumlah_tiket=jumlah_tiket,
            nomor_kursi=nomor_kursi,
            urutan_antrean=urutan_antrean,
            judul_film=judul_film,
            customer_id=customer_id,
        )

        # Jika list kosong, buatkan head & tail dengan node baru
        if self.isEmpty():
            self.head = self.tail = new_node
            return

        # Buat link baru, lalu masukkan node baru ke posisi terakhir
        self.tail.next = new_node
        self.tail = new_node

    # ------------------------------
    # Nama fungsi: isEmpty
    # Penjelasan fungsi : Mengecek apakah linked list pemesanan kosong atau tidak.
    # ------------------------------
    def isEmpty(self):
        "Mengecek apakah linked list kosong."
        # True jika head belum menunjuk ke node manapun
        return self.head is None

    # ------------------------------
    # Nama fungsi: showTickets
    # Penjelasan fungsi : Menampilkan seluruh record pemesanan
    # dalam bentuk tabel menggunakan rich.
    # ------------------------------
    def showTickets(self):
        "Menampilkan seluruh daftar pemesanan tiket."

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
        table.add_column("Nomor Kursi", width=25)
        table.add_column("Tanggal", width=20)

        # Traversal linked list dan tampilkan setiap record ke tabel
        current = self.head
        i = 1

        while current:
            table.add_row(
                str(i),
                current.nama,
                str(current.jumlah_tiket),
                str(" | ".join(current.nomor_kursi)),
                str(current.create_at),
            )
            current = current.next
            i += 1

        console.print(table)

    # ------------------------------
    # Nama fungsi: deleteTicket
    # Penjelasan fungsi : Menghapus satu record pemesanan dari linked list
    # berdasarkan nama customer.
    # ------------------------------
    def deleteTicket(self, nama):
        """
        Menghapus record pemesanan berdasarkan nama.

        Args:
            nama (str): Nama customer yang akan dihapus.

        Returns:
            tuple: (jumlah_tiket, nomor_kursi) yang dikembalikan, atau (None, None) jika tidak ditemukan.
        """
        current = self.head  # Variabel sementara dari awal node

        # Jika nama ditemukan di awal node, hapuskan dan return jumlah tiket customer
        if current and current.nama.strip().lower() == nama.strip().lower():
            self.head = current.next
            return current.jumlah_tiket, current.nomor_kursi

        # Traverse dari awal hingga ketemu nama
        prev = None
        while current and current.nama.strip().lower() != nama.strip().lower():
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
    # Penjelasan fungsi : Mencari satu record pemesanan dalam linked list.
    # Jika ditemukan, menampilkan detail pemesanan dalam bentuk tabel.
    # ------------------------------
    def searchTicket(self, nama):
        """
        Mencari record pemesanan berdasarkan nama.

        Args:
            nama (str): Nama customer yang dicari.

        Returns:
            bool: True jika ditemukan, False jika tidak.
        """

        current = self.head
        found = False
        console = Console()

        # Iterasi seluruh list dan tampilkan detail untuk node yang cocok
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

    # ------------------------------
    # Nama fungsi: deleteTicketByComposite
    # Penjelasan fungsi : Menghapus record pemesanan berdasarkan
    # composite key (nama + jumlah tiket + nomor kursi) untuk
    # menangani kasus nama duplikat.
    # ------------------------------
    def deleteTicketByComposite(
        self, nama: str, jumlah_tiket: int | str = None, nomor_kursi: list = None
    ):
        """
        Menghapus record pemesanan berdasarkan composite key.

        Args:
            nama (str): Nama customer.
            jumlah_tiket (int | str, optional): Jumlah tiket customer (string dari file atau int dari node).
            nomor_kursi (list, optional): Daftar nomor kursi customer.

        Returns:
            tuple: (jumlah_tiket, nomor_kursi) yang dikembalikan, atau (None, None) jika tidak ditemukan.
        """
        current = self.head

        # Traversal list dan cocokkan composite key
        while current is not None:
            # Skip node dengan nama yang tidak cocok
            if current.nama.strip().lower() != nama.strip().lower():
                current = current.next
                continue

            # Cek jumlah_tiket jika disediakan (normalisasi ke int untuk perbandingan robust)
            if jumlah_tiket is not None and current.jumlah_tiket != int(jumlah_tiket):
                current = current.next
                continue

            # Cek nomor_kursi jika disediakan (strip spasi dan ignore urutan)
            if nomor_kursi is not None:
                kursi_normalized = [k.strip() for k in nomor_kursi if k and k.strip()]
                current_normalized = [
                    k.strip() for k in current.nomor_kursi if k and k.strip()
                ]
                if sorted(current_normalized) != sorted(kursi_normalized):
                    current = current.next
                    continue

            # Jika sampai sini, node cocok
            refunded_ticket = current.jumlah_tiket
            refunded_seat = current.nomor_kursi

            # Hapus node dari linked list (handle kasus head & non-head)
            if current == self.head:
                self.head = current.next
                if self.head is None:
                    self.tail = None
            else:
                # Cari node sebelum current untuk menyambungkan list
                prev = self.head
                while prev.next != current:
                    prev = prev.next
                prev.next = current.next
                if current.next is None:
                    self.tail = prev

            return refunded_ticket, refunded_seat

        return None, None
