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

# ------------------------------
# Nama fungsi: showFilm
# Penjelasan fungsi : Untuk menampilkan daftar film.
# ------------------------------
def showFilm() -> str:
    """
    Menampilkan daftar film yang tersedia

    Returns:
        str: film_id yang dipilih oleh user
    """
    # Cetak title
    print("==== Daftar Film ====")

    # Ambil data untuk cetak judul film
    data_film = getAllData("data_film")
    no = 1

    # Menyimpan film id
    film_ids = []

    # Cetak judul film
    for film_id, data_film in data_film.items():
        # Cetak judul film
        print(f"{no}. {data_film['judul_film']}")

        # Tambah id ke film_ids
        film_ids.append(film_id)

        # Iterasi nomor urutan
        no += 1

    # Result id film
    pilih = input("\nPilih : ").strip()

    # Input validator dan return
    if pilih.isdigit() and int(pilih) <= len(film_ids) and int(pilih) > 0:
        return film_ids[int(pilih) - 1]
    else:
        return
# ------------------------------
# Nama fungsi: updateFilm
# Penjelasan fungsi : Untuk untuk menganti judul film dan kuota penonton film serta menyimpannya ke file .txt.
# ------------------------------
def updateFilm(judul_film: str, kuota_penonton: int, film_id: str):
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

    # Success message
    print("Film berhasil diupdate!")

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
        print(f"Film `{deleted['judul_film']}`, berhasil dihapus!")

        # Rewritte pada database
        updateData(data_dict=data_film, data_name="data_film")
    else:
        print("Film gagal dihapus!")

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

    # Success message
    print("Film berhasil ditambahkan!")
    