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
7. countNameInQueue (internal use only [helper method untuk cancelQueue])
8. adjustAntrean (internal use only [helper method untuk cancelQueue])
==========================================================
"""

# Import pandas untuk menampilkan queue
import pandas as pd

# Import class Node untuk membuat node yang akan digunakan pada queue
from CRUD.utils.node import Node


# ````````````````````````````````````````````
# Nama kelas: Queue
# Penjelasan kelas : Untuk membuat queue yang akan digunakan untuk mengelola antrean tiket.
# ````````````````````````````````````````````
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

        # untuk memberikan nomor urut pada setiap node yang masuk ke antrean
        self.urutan = 1

    # ===============================
    # Nama fungsi: isEmpty
    # Penjelasan fungsi : Untuk mengecek apakah antrean kosong.
    # ===============================
    def isEmpty(self):
        "Ketika queue kosong maka front -> rear -> none"
        return self.front is None

    # ===============================
    # Nama fungsi: enqueue
    # Penjelasan fungsi : Untuk menambahkan client ke antrean
    #                     (menambahkan data baru ke bagian belakang).
    # ===============================
    def enqueue(self, nama: str):
        """
        Menambahkan data baru ke bagian belakang antrean (rear)\n
        Setiap data baru yang masuk ke antrean akan mendapatkan nomor urut yang bertambah

        Args:
            nama (str): Nama client yang akan ditambahkan ke antrean
        """
        new_node = Node(nama, urutan_antrean=self.urutan)

        # Setiap data baru yang masuk ke antrean akan mendapatkan
        # nomor urut yang bertambah 1 dari data sebelumnya
        self.urutan += 1

        # Jika data baru masuk dari queue yang kosong maka data baru -> rear
        if self.isEmpty():
            self.front = new_node
            self.rear = new_node
            return

        # Jika queue tidak kosong, maka data baru diletakkan
        # setelah rear kemudian dijadikan sebagai rear
        self.rear.next = new_node
        self.rear = new_node

    # ===============================
    # Nama fungsi: updateQueue
    # Penjelasan fungsi : Untuk memperbarui data pada node
    #                     yang ada dalam antrean pada fase layani antrean.
    # ===============================
    def updateQueue(self, jumlah_tiket: int, nomor_kursi: list, judul_film: str):
        """
        Mengupdate data pada node yang ada dalam antrean pada fase layani antrean\n
        Hanya untuk node bagian front (data yang sedang dilayani)

        Args:
            jumlah_tiket (int): Jumlah tiket yang dipesan oleh client
            nomor_kursi (list): Nomor kursi yang dipesan oleh client
            judul_film (str): Judul film yang ditonton oleh client
        """
        # Jika antrean kosong, maka tidak ada data yang bisa diperbarui
        if self.isEmpty():
            print("Antrean kosong!")
            return None

        # Mengupdate data pada node bagian front (data yang sedang dilayani)
        self.front.jumlah_tiket = jumlah_tiket
        self.front.nomor_kursi = nomor_kursi
        self.front.judul_film = judul_film

    # ================================
    # Nama fungsi: dequeue
    # Penjelasan fungsi : Untuk menghapus client dari antrean (menghapus data paling depan).
    # ================================
    def dequeue(self) -> Node | None:
        """
        Menghapus data paling depan dari antrean (front)\n
        Data yang dihapus merupakan data yang sedang dilayani, sehingga\n
        data tersebut akan diproses terlebih dahulu sebelum dihapus

        Returns:
            Node: Node yang dihapus dari antrean (data yang sedang dilayani)
        """

        # Jika antrean kosong, maka tidak ada data yang bisa dihapus
        if self.isEmpty():
            print("Antrean kosong!")
            return None

        # lihat data bagian front, simpan di variable data yang akan diinput (dilayani)
        node_dilayani = self.front

        # geser pointer front ke next front
        self.front = self.front.next

        # Jika setelah menggeser pointer front, front menjadi None, maka rear juga
        # harus diubah menjadi None (antrean menjadi kosong)
        if self.front is None:
            self.rear = None

        return node_dilayani

    # ===============================
    # Nama fungsi: showQueue
    # Penjelasan fungsi : Untuk menampilkan antrean.
    # ===============================
    def showQueue(self):
        """
        Menampilkan data dalam antrean
        """

        # Jika antrean kosong, maka tidak ada data yang bisa ditampilkan
        if self.isEmpty():
            print("Antrean kosong!")
            return

        # Menginisialisasi list untuk menyimpan data antrean yang akan ditampilkan
        data = []
        current = self.front

        # Melakukan iterasi untuk mengambil data dari setiap node dalam antrean dan
        # menyimpannya dalam list data
        while current is not None:
            data.append(current.nama)
            current = current.next

        # Set data antrean ke dalam data frame untuk ditampilkan
        df = pd.DataFrame(data, columns=["Nama"])

        # Menambah urutan angka ke kolom pertama data frame
        df.insert(0, "NO", range(1, len(df) + 1))

        # Mencetak title dan data frame daftar antrean
        print("====== Daftar Antrean ======")
        print(df.to_string(index=False))

    # ===============================
    # Nama fungsi: countNameInQueue
    # Penjelasan fungsi : Untuk menghitung jumlah kemunculan nama tertentu dalam antrean.
    # ===============================
    def countNameInQueue(self, nama: str) -> int:
        """
        Menghitung jumlah kemunculan nama tertentu dalam antrean

        Args:
            nama (str): Nama client yang akan dihitung jumlah kemunculannya dalam antrean

        Returns:
            int: Jumlah kemunculan nama dalam antrean
        """
        # Menginisialisasi variabel untuk menyimpan jumlah kemunculan nama
        count = 0

        current = self.front  # Inisialisasi iterasi

        # Melakukan iterasi untuk menghitung jumlah kemunculan nama dalam antrean
        while current is not None:
            if current.nama == nama.lower():
                count += 1
            current = current.next

        return count

    # ================================
    # Nama fungsi : adjustAntrean
    # Penjelasan fungsi : Untuk menyesuaikan nomor urut antrean setelah pembatalan antrean.
    # ================================
    def adjustAntrean(self, start_node):
        """
        Menyesuaikan nomor urut antrean setelah pembatalan antrean\n
        Setelah satu node dalam antrean dibatalkan, maka nomor urut dari node-node setelahnya\n
        harus disesuaikan dengan mengurangi nomor urut sebanyak 1

        Args:
            start_node (Node): Node yang menjadi titik awal penyesuaian nomor urut antrean (node setelah node yang dibatalkan)
        """

        current = start_node

        while current is not None:
            current.urutan_antrean -= 1
            current = current.next

    # ===============================
    # Nama fungsi: cancelQueue
    # Penjelasan fungsi : Untuk membatalkan satu node dalam antrean (queue)
    # ===============================
    def cancelQueue(self, nama: str):
        """
        Membatalkan satu node dalam antrean (queue)\n
        Data yang dibatalkan akan dihapus dari antrean, sehingga data tersebut tidak akan dilayani

        Args:
            nama (str): Nama client yang akan dibatalkan dari antrean
        Returns:
            nama (str): Nama client yang dibatalkan dari antrean
            urutan_batal (int): Urutan saat client dibatalkan
        """

        # Inisialisasi fungsi countNameInQueue untuk menentukan step mana yang akan berjalan
        count_nama = self.countNameInQueue(nama)

        # Inisialisasi variabel urutan batal
        urutan_batal = 0

        # Jika terdapat lebih dari 1 data dengan nama yang sama dalam antrean,
        # maka dapat ditentukan dengan urutan antrean
        if count_nama > 1:
            # Mencetak jumlah data dengan nama yang sama dalam antrean
            print(
                f"\nTerdapat {count_nama} data dengan nama '{nama}' dalam antrean.")

            # Melakukan iterasi untuk mencari data dengan nama yang sama dalam antrean,
            # menampilkan urutan antreannya, dan menyimpan urutannya
            current = self.front
            urutan_list = []
            while current is not None:
                if current.nama == nama:
                    print(
                        f"Urutan : {current.urutan_antrean}, nama: {current.nama}, waktu masuk antrean : {current.create_at}"
                    )
                urutan_list.append(current.urutan_antrean)
                current = current.next

            while True:  # Loop hingga input valid
                # Meminta input urutan antrean yang akan dibatalkan
                urutan_batal = input(
                    "\nNomor antrean yang akan dibatalkan (Enter untuk kembali) : "
                ).strip()

                # Jika user menekan Enter tanpa memasukkan nomor antrean, maka batal membatalkan
                # antrean dan kembali ke menu sistem antrean
                if not urutan_batal:
                    return
                try:
                    urutan_batal = int(urutan_batal)
                except ValueError:
                    print("Urutan antrean tidak valid!")
                    continue

                # Validasi apakah input urutan batal ada di list
                if urutan_batal in urutan_list:
                    break

            # Jika data yang dibatalkan merupakan data bagian front
            if self.front.nama == nama and self.front.urutan_antrean == urutan_batal:
                # Geser pointer front ke next front untuk menghapus data bagian front
                self.front = self.front.next

                # Set kembali urutan_antrean
                self.adjustAntrean(self.front)
                return nama, urutan_batal

            # Melakukan iterasi untuk mencari data dengan nama dan
            # urutan antrean yang sesuai untuk dibatalkan
            current = self.front
            while current is not None:
                if (
                    current.next.nama == nama
                    and current.next.urutan_antrean == urutan_batal
                ):
                    # Jika data ditemukan, maka data tersebut dihapus dari antrean dengan
                    # mengubah pointer next dari node sebelumnya ke node setelahnya
                    current.next = current.next.next

                    # Jika data yang dibatalkan merupakan data bagian rear,
                    # maka rear juga harus diubah menjadi node sebelumnya
                    if current.next is None:
                        self.rear = current

                    # Setelah data dibatalkan, maka nomor urut dari node-node setelahnya harus
                    # disesuaikan dengan mengurangi nomor urut sebanyak 1
                    self.adjustAntrean(current.next)

                    return nama, urutan_batal
                current = current.next

        # Jika hanya terdapat 1 nama dalam antrean
        else:
            # Jika data yang dibatalkan merupakan data bagian front
            if self.front.nama == nama:
                # Geser pointer front ke next front untuk menghapus data bagian front
                self.front = self.front.next

                # Set kembali urutan_antrean
                self.adjustAntrean(self.front)

                return nama, urutan_batal

            # Melakukan iterasi untuk mencari data yang akan dibatalkan dalam antrean
            current = self.front
            while current.next is not None:
                if current.next.nama == nama:
                    # Jika data ditemukan, maka data tersebut dihapus dari antrean dengan
                    # mengubah pointer next dari node sebelumnya ke node setelahnya
                    current.next = current.next.next

                    # Jika data yang dibatalkan merupakan data bagian rear, maka rear juga harus
                    # diubah menjadi node sebelumnya
                    if current.next is None:
                        self.rear = current

                    # Setelah data dibatalkan, maka nomor urut dari node-node setelahnya harus
                    # disesuaikan dengan mengurangi nomor urut sebanyak 1
                    self.adjustAntrean(current.next)

                    return nama, urutan_batal
                current = current.next

        # Jika nama tidak ditemukan, return data kosong
        return None, urutan_batal
