"""
==========================================================
Main Menu
Berisi menu sistem kontrol dan navigasi untuk ke fitur

Kontributor : Wildhan Dzikrihantara, M. Lutfi Ramadhan Warendra
Fungsi/fitur:
1. main
2. sistemAntrean
3. pilihFilm
==========================================================

"""

# Import features yang akan digunakan di main 

# queue
# from CRUD.operations.queue import Queue

# linked list
# from CRUD.operations.linkedList import LinkedList

# order
from CRUD.operations.order import orderKursi, storeOrder, resetOrder

# film
from CRUD.operations.film import showFilm, addFilm, updateFilm, deleteFilm

# invoice
from CRUD.operations.invoice import invoice

# utillities & libraries
# from CRUD.utils.nodeGenerator import generateNode
from CRUD.utils.idGenerator import generateID
from CRUD.utils.dataOps import getAllData, searchData, updateData

# ------------------------------
# Nama fungsi: pilihFilm
# Penjelasan fungsi : Untuk memilih film yang akan dimanage sistem anterannya.
# ------------------------------
def pilihFilm():
    pass

# ------------------------------
# Nama fungsi: sistemAntrean
# Penjelasan fungsi : Untuk memanage sistem antrian suatu film bioskop.
# ------------------------------
def sistemAntrean():
    pass

# ------------------------------
# Nama fungsi: main
# Penjelasan fungsi : Untuk tampilan dan kontrol main menu.
# ------------------------------
def main():
    pass

# Untuk menjalankan fungsi main secara langsung
if __name__ == "__main__":
    main()