"""
==========================================================
Node
Membuat node untuk digunakan pada linked list dan queue

Class:
1. Node
==========================================================
"""

from datetime import datetime


# ````````````````````````````````````````````
# Nama kelas: Node
# Penjelasan kelas : Untuk membuat node yang akan digunakan pada linked list dan queue.
# ````````````````````````````````````````````
class Node:
    """
    Class Node: data customer pemesanan antrean tiket bioskop

    Atribut:
        nama: str (nama customer)
        jumlah_tiket: int (jumlah tiket yang dipesan)
        nomor_kursi: list (nomor kursi yang dipesan)
        urutan_antrean: int (urutan dalam antrean)
        judul_film: str (judul film yang ditonton)
        create_at: str (waktu pembuatan record)
    """

    # ===============================
    # Nama fungsi: __init__
    # Penjelasan fungsi : Untuk menginisialisasi atribut pada node.
    # ===============================
    def __init__(
        self,
        nama: str,
        jumlah_tiket: int = None,
        nomor_kursi: list = None,
        urutan_antrean: int = None,
        judul_film: str = None,
        film_id: str = None,
        customer_id: str = None,
    ):
        self.customer_id = customer_id
        self.film_id = film_id
        self.nama = nama.lower()
        self.jumlah_tiket = jumlah_tiket
        self.nomor_kursi = nomor_kursi
        self.urutan_antrean = urutan_antrean
        self.judul_film = judul_film
        self.create_at = datetime.now().strftime("%d/%m/%y - %H:%M:%S")
        self.next = None
