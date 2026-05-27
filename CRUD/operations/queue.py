"""
==========================================================
Manajemen Antrean (Queue)
Berisi algoritma queue untuk mengelola antrean tiket bioskop yang terdiri atas beberapa fungsi.

Kontributor : Wildhan Dzikrihantara
Class:
1. Queue

Method:
1. enqueue
2. dequeue
3. isEmpty
4. cancelQueue
5. showQueue
6. updateQueue
7. peek
8. countNameInQueue (internal use only [helper method untuk cancelQueue])
9. adjustAntrean (internal use only [helper method untuk cancelQueue])
==========================================================
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from CRUD.utils.node import Node


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.urutan = 1

    def isEmpty(self):
        "Ketika queue kosong maka front -> rear -> none"
        return self.front is None

    def enqueue(self, nama: str):
        """
        Menambahkan data baru ke bagian belakang antrean (rear)\n
        Setiap data baru yang masuk ke antrean akan mendapatkan nomor urut yang bertambah

        Args:
            nama (str): Nama client yang akan ditambahkan ke antrean
        """
        new_node = Node(nama, urutan_antrean=self.urutan)
        self.urutan += 1

        if self.isEmpty():
            self.front = new_node
            self.rear = new_node
            return

        self.rear.next = new_node
        self.rear = new_node

    def updateQueue(self, jumlah_tiket: int, nomor_kursi: list, judul_film: str):
        """
        Mengupdate data pada node yang ada dalam antrean pada fase layani antrean\n
        Hanya untuk node bagian front (data yang sedang dilayani)

        Args:
            jumlah_tiket (int): Jumlah tiket yang dipesan oleh client
            nomor_kursi (list): Nomor kursi yang dipesan oleh client
            judul_film (str): Judul film yang ditonton oleh client
        """
        if self.isEmpty():
            print("Antrean kosong!")
            return None

        self.front.jumlah_tiket = jumlah_tiket
        self.front.nomor_kursi = nomor_kursi
        self.front.judul_film = judul_film

    def dequeue(self) -> Node | None:
        """
        Menghapus data paling depan dari antrean (front)\n
        Data yang dihapus merupakan data yang sedang dilayani, sehingga\n
        data tersebut akan diproses terlebih dahulu sebelum dihapus

        Returns:
            Node: Node yang dihapus dari antrean (data yang sedang dilayani)
        """

        if self.isEmpty():
            print("Antrean kosong!")
            return None

        node_dilayani = self.front
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return node_dilayani

    def peek(self) -> Node | None:
        """Returns the front node without removing it."""
        return self.front

    def showQueue(self):
        """
        Menampilkan data dalam antrean
        """
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

    def countNameInQueue(self, nama: str) -> int:
        """
        Menghitung jumlah kemunculan nama tertentu dalam antrean

        Args:
            nama (str): Nama client yang akan dihitung jumlah kemunculannya dalam antrean

        Returns:
            int: Jumlah kemunculan nama dalam antrean
        """
        count = 0
        current = self.front

        while current is not None:
            if current.nama == nama.lower():
                count += 1
            current = current.next

        return count

    def adjustAntrean(self, start_node):
        """
        Menyesuaikan nomor urut antrean setelah pembatalan antrean\n

        Args:
            start_node (Node): Node yang menjadi titik awal penyesuaian nomor urut antrean (node setelah node yang dibatalkan)
        """

        current = start_node

        while current is not None:
            current.urutan_antrean -= 1
            current = current.next

    def cancelQueue(self, nama: str):
        """
        Membatalkan satu node dalam antrean (queue)\n

        Args:
            nama (str): Nama client yang akan dibatalkan dari antrean
        Returns:
            nama (str): Nama client yang dibatalkan dari antrean
            urutan_batal (int): Urutan saat client dibatalkan
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
