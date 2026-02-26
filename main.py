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

import pandas as pd

# ------------------------------
# Nama fungsi: pilihFilm
# Penjelasan fungsi : Untuk memilih film yang akan dimanage sistem anterannya.
# ------------------------------
def pilihFilm() -> str | None:
    # Menampilkan header
    print("==== PILIH FILM =====")
    
    # Mengambil data_film dari database
    data_film = getAllData("data_film")
    
    # Memasukan data_film ke data frame untuk ditampilkan
    df = pd.DataFrame(data_film).T
    
    # Memodifikasi data frame
    df.drop(columns=["kuota_penonton"], inplace=True) # Menghilangkan kuota_penonton dari data frame
    df.rename(columns={"judul_film": "JUDUL FILM"}, inplace=True) # Mengganti title judul_film -> JUDUL FILM
    df.insert(0, "NO", range(1, len(df)+1)) # Menambah urutan angka ke kolom 1 data frame

    # Menampilkan data frame
    print(df.to_string(index=False))
    
    # Meminta pilihan judul film
    pilih = input("\nPilih Nomor : ")
    
    # Validasi tipe input, jika tidak berupa angka tanyakan kembali
    while not pilih.isdigit():
        print("Input harus berupa angka.")
        pilih = input("\nPilih Nomor : ")
        
    # Mengubah input plih ke integer
    pilih = int(pilih)
    
    # Validasi urutan input
    if 1 <= pilih <= len(data_film):
        # Ambil ID sesuai urutan
        film_id = list(data_film.keys())[pilih - 1]
        
        return film_id
    else:
        print("Nomor urut tidak valid.")
        return

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