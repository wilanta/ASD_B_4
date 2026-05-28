"""
==========================================================
Manajemen Daftar Film
CRUD (Create, Read, Update, Delete) untuk mengelola
daftar film bioskop: menambah, mengubah, dan menghapus film.

Kontributor : M. Lutfi Ramadhan Warendra

Fungsi/fitur:
1. pilihFilm   - Menampilkan daftar film dan memilih salah satu
2. addFilm     - Menambahkan film baru ke database
3. updateFilm  - Mengubah judul dan/atau kuota penonton film
4. deleteFilm  - Menghapus film dari database
==========================================================
"""

# External
from rich import print
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Utils
from CRUD.utils.clear import _clear

# Utilities
from CRUD.utils.idGenerator import generateID
from CRUD.utils.dataOps import getAllData, updateData

# ------------------------------
# Nama fungsi: pilihFilm
# Penjelasan fungsi : Menampilkan daftar film yang tersedia
# dan mengembalikan ID film yang dipilih oleh user.
# ------------------------------


def pilihFilm() -> str | None:
    """
    Memilih film dan mengembalikan string ID film dari database.

    Return:
        id (str): id film.
    """
    _clear()

    # Menampilkan header
    print("\n\n[bold white]Pilih Film[/bold white]")
    print("[dim]Pilih untuk melanjutkan.[/dim]\n")

    # Mengambil data_film dari database
    data_film = getAllData("data_film")

    # Memasukan judul film ke list
    title_list = [data["judul_film"] for data in data_film.values()]
    title_list.append(Choice(value=None, name="--- Keluar ---"))

    # Validasi apakah film ada
    if data_film == {}:
        # Status film kosong
        console = Console()

        console.print(
            Panel(
                "[bold red]Film kosong![/bold red]",
                title="[bold red]Daftar Film[/bold red]",
                border_style="red",
            )
        )

    # Menampilkan pilihan dan meminta pilihan dari user
    choice = inquirer.select(
        message="",
        choices=title_list,
        default="Auto (match terminal)",
        pointer=">",
        instruction="Gunakan ↑ ↓ untuk memindahkan opsi, Enter untuk memilih",
    ).execute()

    film_id = next(
        (
            id_film
            for id_film, data in data_film.items()
            if data["judul_film"] == choice
        ),
        None,
    )

    return film_id


# ------------------------------
# Nama fungsi: updateFilm
# Penjelasan fungsi : Mengubah judul film dan/atau kuota penonton,
# lalu menyimpan perubahan ke file data_film.txt.
# ------------------------------
def updateFilm(judul_film: str, kuota_penonton: int, film_id: str):
    """
    Mengubah judul film dan/atau kuota penonton.

    Args:
        judul_film (str): Judul film baru (kosongkan untuk tidak mengubah).
        kuota_penonton (int): Kuota penonton baru (kosongkan untuk tidak mengubah).
        film_id (str): ID film yang akan diubah.
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
# Penjelasan fungsi : Menghapus satu film dari database berdasarkan ID.
# ------------------------------
def deleteFilm(film_id):
    """
    Menghapus film dari database berdasarkan ID.

    Args:
        film_id (str): ID film yang akan dihapus.
    """

    # Ambil data dari database
    data_film = getAllData("data_film")

    # Delete data target
    deleted = data_film.pop(film_id, None)

    # Message status
    if deleted:
        _clear()
        print(f'Film "{deleted["judul_film"]}", berhasil dihapus!')

        # Rewritte pada database
        updateData(data_dict=data_film, data_name="data_film")


# ------------------------------
# Nama fungsi: addFilm
# Penjelasan fungsi : Menambahkan film baru ke database dan menyimpannya
# ke file data_film.txt.
# ------------------------------
def addFilm(judul: str, kuota_penonton: int):
    """
    Menambahkan film baru ke database.

    Args:
        judul (str): Judul film.
        kuota_penonton (int): Kuota/kapasitas penonton.
    """

    # Mengambil data dari database agar data baru tidak menimpa data lama
    data_film = getAllData("data_film")

    # Simpan data terbaru ke dict data_film
    data_film[generateID()] = {
        "judul_film": judul,
        "kuota_penonton": kuota_penonton,
    }

    # Memanggil fungsi updateData untuk menyimpan data film baru ke file data_film.txt
    updateData(data_dict=data_film, data_name="data_film")
