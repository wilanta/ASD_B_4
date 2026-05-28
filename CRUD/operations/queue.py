"""
==========================================================
Manajemen Antrean (Queue)
Berisi struktur data queue (antrean FIFO) untuk mengelola
urutan pelayanan tiket bioskop.

Kontributor : Wildhan Dzikrihantara

Class:
1. Queue

Method:
1. enqueue       - Menambahkan customer ke belakang antrean
2. dequeue       - Menghapus customer dari depan antrean
3. isEmpty       - Mengecek apakah antrean kosong
4. cancelQueue   - Membatalkan satu antrean berdasarkan nama
5. showQueue     - Menampilkan seluruh daftar antrean
6. updateQueue   - Memperbarui data customer di depan antrean
7. peek          - Melihat customer terdepan tanpa menghapus
8. countNameInQueue    - Menghitung kemunculan nama dalam antrean
9. adjustAntrean       - Menyesuaikan nomor urut setelah pembatalan
==========================================================
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from CRUD.utils.node import Node


# ------------------------------
# Nama kelas: Queue
# Penjelasan kelas : Struktur data antrean (FIFO) untuk mengelola
# urutan pelayanan customer di bioskop.
# ------------------------------
class Queue:
    # ------------------------------
    # Nama fungsi: __init__
    # Penjelasan fungsi : Inisialisasi struktur antrean kosong.
    # ------------------------------
    def __init__(self):
        self.front = None
        self.rear = None
        self.urutan = 1

    # ------------------------------
    # Nama fungsi: __init__
    # Penjelasan fungsi : Inisialisasi struktur antrean kosong.
    # ------------------------------
    def __init__(self):
        self.front = None
        self.rear = None
        self.urutan = 1

    # ------------------------------
    # Nama fungsi: isEmpty
    # Penjelasan fungsi : Mengecek apakah antrean dalam kondisi kosong.
    # ------------------------------
    def isEmpty(self):
        "Mengecek apakah antrean kosong."
        return self.front is None

    # ------------------------------
    # Nama fungsi: peek
    # Penjelasan fungsi : Melihat data customer di depan antrean
    # tanpa menghapusnya dari antrean.
    # ------------------------------
    def peek(self) -> Node | None:
        "Mengembalikan node terdepan tanpa menghapusnya."
        return self.front

    # ------------------------------
    # Nama fungsi: enqueue
    # Penjelasan fungsi : Menambahkan customer baru ke belakang antrean (rear).
    # Setiap customer baru mendapatkan nomor urutan yang bertambah.
    # ------------------------------
    def enqueue(self, nama: str):
        """
        Menambahkan customer baru ke belakang antrean (rear).
        Setiap customer baru mendapatkan nomor urut yang bertambah.

        Args:
            nama (str): Nama customer yang ditambahkan ke antrean.
        """
        new_node = Node(nama, urutan_antrean=self.urutan)
        self.urutan += 1

        if self.isEmpty():
            self.front = new_node
            self.rear = new_node
            return

        self.rear.next = new_node
        self.rear = new_node

    # ------------------------------
    # Nama fungsi: updateQueue
    # Penjelasan fungsi : Memperbarui data customer di depan antrean
    # pada fase layani antrean (hanya node front).
    # ------------------------------
    def updateQueue(self, jumlah_tiket: int, nomor_kursi: list, judul_film: str):
        """
        Memperbarui data customer di depan antrean.

        Args:
            jumlah_tiket (int): Jumlah tiket yang dipesan.
            nomor_kursi (list): Nomor kursi yang dipesan.
            judul_film (str): Judul film yang ditonton.
        """
        if self.isEmpty():
            print("Antrean kosong!")
            return None

        self.front.jumlah_tiket = jumlah_tiket
        self.front.nomor_kursi = nomor_kursi
        self.front.judul_film = judul_film

    # ------------------------------
    # Nama fungsi: dequeue
    # Penjelasan fungsi : Menghapus dan mengembalikan customer di depan antrean.
    # Customer yang dihapus adalah yang sedang dilayani.
    # ------------------------------
    def dequeue(self) -> Node | None:
        """
        Menghapus dan mengembalikan customer di depan antrean.

        Returns:
            Node | None: Node customer yang dilayani, atau None jika antrean kosong.
        """

        if self.isEmpty():
            print("Antrean kosong!")
            return None

        node_dilayani = self.front
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return node_dilayani

    # ------------------------------
    # Nama fungsi: showQueue
    # Penjelasan fungsi : Menampilkan seluruh daftar antrean dalam bentuk tabel.
    # ------------------------------
    def showQueue(self):
        console = Console()

        if self.isEmpty():
            console.print(
                Panel(
                    "[bold red]Antrean kosong![/bold red]",
                    title="[bold red]Daftar Antrean[/bold red]",
                    border_style="red",
                )
            )
            return

        table = Table(
            title="Daftar Antrean",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            expand=False,
        )

        table.add_column("No", justify="center", width=6)
        table.add_column("Nama", justify="left")

        current = self.front
        no = 1

        while current is not None:
            table.add_row(str(no), current.nama)
            current = current.next
            no += 1

        console.print(table)

    # ------------------------------
    # Nama fungsi: countNameInQueue
    # Penjelasan fungsi : Menghitung jumlah kemunculan nama tertentu dalam antrean.
    # Helper internal untuk cancelQueue.
    # ------------------------------
    def countNameInQueue(self, nama: str) -> int:
        """
        Menghitung kemunculan nama dalam antrean.

        Args:
            nama (str): Nama yang ingin dihitung.

        Returns:
            int: Jumlah kemunculan nama.
        """
        count = 0
        current = self.front

        while current is not None:
            if current.nama == nama.lower():
                count += 1
            current = current.next

        return count

    # ------------------------------
    # Nama fungsi: adjustAntrean
    # Penjelasan fungsi : Menyesuaikan nomor urut antrean بعد pembatalan.
    # Mengurangi urutan semua node setelah node yang dibatalkan.
    # Helper internal untuk cancelQueue.
    # ------------------------------
    def adjustAntrean(self, start_node):
        """
        Menyesuaikan nomor urut antrean setelah pembatalan.

        Args:
            start_node: Node yang menjadi titik awal penyesuaian.
        """

        current = start_node

        while current is not None:
            current.urutan_antrean -= 1
            current = current.next

    # ------------------------------
    # Nama fungsi: cancelQueue
    # Penjelasan fungsi : Membatalkan satu customer dari antrean berdasarkan nama.
    # Jika ada lebih dari satu customer dengan nama yang sama,
    # akan diminta memilih urutan yang akan dibatalkan.
    # ------------------------------
    def cancelQueue(self, nama: str):
        """
        Membatalkan satu customer dari antrean.

        Args:
            nama (str): Nama customer yang akan dibatalkan.

        Returns:
            tuple: (nama, urutan_batal) atau (None, urutan_batal) jika tidak ditemukan.
        """

        count_nama = self.countNameInQueue(nama)
        urutan_batal = 0

        if count_nama > 1:
            print(f"\nTerdapat {count_nama} data dengan nama '{nama}' dalam antrean.")

            current = self.front
            urutan_list = []
            while current is not None:
                if current.nama == nama:
                    print(
                        f"Urutan : {current.urutan_antrean}, nama: {current.nama}, waktu masuk antrean : {current.create_at}"
                    )
                urutan_list.append(current.urutan_antrean)
                current = current.next

            while True:
                urutan_batal = input(
                    "\nNomor antrean yang akan dibatalkan (Enter untuk kembali) : "
                ).strip()

                if not urutan_batal:
                    return
                try:
                    urutan_batal = int(urutan_batal)
                except ValueError:
                    print("Urutan antrean tidak valid!")
                    continue

                if urutan_batal in urutan_list:
                    break

            if self.front.nama == nama and self.front.urutan_antrean == urutan_batal:
                self.front = self.front.next
                self.adjustAntrean(self.front)
                return nama, urutan_batal

            current = self.front
            while current is not None:
                if (
                    current.next.nama == nama
                    and current.next.urutan_antrean == urutan_batal
                ):
                    current.next = current.next.next

                    if current.next is None:
                        self.rear = current

                    self.adjustAntrean(current.next)

                    return nama, urutan_batal
                current = current.next

        else:
            if self.front.nama == nama:
                self.front = self.front.next
                self.adjustAntrean(self.front)
                return nama, urutan_batal

            current = self.front
            while current.next is not None:
                if current.next.nama == nama:
                    current.next = current.next.next

                    if current.next is None:
                        self.rear = current

                    self.adjustAntrean(current.next)

                    return nama, urutan_batal
                current = current.next

        return None, urutan_batal
