"""
==========================================================
Manajemen Daftar Film
Mengelola film seperti menambahkan judul, mengubah judul/kuota penonton, dan menghapus judul film

Kontributor : M. Lutfi Ramadhan Warendra
Fungsi/fitur:
1. showFilm
2. updateFilm
3. deleteFilm
4. addFilm
==========================================================
"""
# External
import pandas as pd

# Utilities
from CRUD.utils.idGenerator import generateID
from CRUD.utils.dataOps import getAllData, updateData

# ------------------------------
# Nama fungsi: pilihFilm
# Penjelasan fungsi : Untuk memilih film yang akan dimanage sistem anterannya.
# ------------------------------


def pilihFilm() -> str | None:
    """
    Memilih film dan mengembalikan string ID film dari database.

    Return:
        id (str): id film.
    """

    # Menampilkan header
    print("==== PILIH FILM =====")

    # Mengambil data_film dari database
    data_film = getAllData("data_film")

    # Memasukan data_film ke data frame untuk ditampilkan
    df = pd.DataFrame(data_film).T

    # Memodifikasi data frame
    df.drop(
        columns=["kuota_penonton"], inplace=True
    )  # Menghilangkan kuota_penonton dari data frame
    df.rename(
        columns={"judul_film": "JUDUL FILM"}, inplace=True
    )  # Mengganti title judul_film -> JUDUL FILM
    df.insert(
        0, "NO", range(1, len(df) + 1)
    )  # Menambah urutan angka ke kolom 1 data frame

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


# ------------------------------
# Nama fungsi: updateFilm
# Penjelasan fungsi : Untuk untuk menganti judul film dan kuota penonton film serta menyimpannya ke file .txt.
# ------------------------------
def updateFilm(judul_film: str, kuota_penonton: int, film_id: str):
    """
    Meng-update judul film dan kuota penonton.
    
    Args:
        judul_film (str): Judul Film
        kuota_penonton (str): Kuota Penonton
        film_id (str): ID Film
    """
    
    # Mengambil data dari database agar data lainnya tidak terhapus
    data_film = getAllData("data_film")

    # Validasi input, jika input kosong maka pakai data yang lama
    judul = judul_film if judul_film != "" else data_film[film_id]["judul_film"]
    kuota = (
        kuota_penonton if kuota_penonton != "" else data_film[film_id]["kuota_penonton"]
    )

    # Simpan data terbaru ke dict data_film
    data_film[film_id] = {
        "judul_film": judul,
        "kuota_penonton": kuota,
    }

    # Memanggil fungsi updateData untuk menyimpan update data film ke file data_film.txt
    updateData(data_dict=data_film, data_name="data_film")


# ------------------------------
# Nama fungsi: deleteFilm
# Penjelasan fungsi : Untuk menghapus film dari daftar film serta menyimpannya ke file .txt.
# ------------------------------
def deleteFilm(film_id):
    # Ambil data dari database
    data_film = getAllData("data_film")

    # Delete data target
    deleted = data_film.pop(film_id, None)

    # Message status
    if deleted:
        print(f"Film \"{deleted['judul_film']}\", berhasil dihapus!")

        # Rewritte pada database
        updateData(data_dict=data_film, data_name="data_film")


# ------------------------------
# Nama fungsi: addFilm
# Penjelasan fungsi : Untuk menambahkan film ke daftar film serta menyimpannya ke file data_film.txt.
# ------------------------------
def addFilm(judul: str, kuota_penonton: int):
    # Mengambil data dari database agar data baru tidak menimpa data lama
    data_film = getAllData("data_film")

    # Simpan data terbaru ke dict data_film
    data_film[generateID()] = {
        "judul_film": judul,
        "kuota_penonton": kuota_penonton,
    }

    # Memanggil fungsi updateData untuk menyimpan data film baru ke file data_film.txt
    updateData(data_dict=data_film, data_name="data_film")
