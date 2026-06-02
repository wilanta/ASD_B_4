from CRUD.utils.dataOps import getAllData, updateData
from CRUD.utils.seatSort import seat_sort


# ------------------------------
# Nama fungsi: deleteTempPemesanan
# Penjelasan fungsi : Menghapus semua record pemesanan sementara
# dari temp_log_pemesanan.txt berdasarkan judul film.
# ------------------------------
def deleteTempPemesanan(judul_film: str):
    """
    Menghapus record pemesanan sementara berdasarkan judul film.

    Args:
        judul_film (str): Judul film yang record-nya akan dihapus.
    """

    # Mengambil semua data dari database
    temp_pemesanan_data = getAllData("temp_log_pemesanan")

    # Menyaring data agar hanya menyisakan record yang BUKAN film ini
    temp_pemesanan_data = {
        log_id: data
        for log_id, data in temp_pemesanan_data.items()
        if data["judul"] != judul_film
    }

    updateData(temp_pemesanan_data, "temp_log_pemesanan")


# ------------------------------
# Nama fungsi: deleteTempSeat
# Penjelasan fungsi : Menghapus semua record pemesanan sementara
# dari temp_seat.txt berdasarkan judul film.
# ------------------------------
def deleteTempSeat(judul_film: str):
    """
    Menghapus record seat berdasarkan judul film.

    Args:
        judul_film (str): Judul film yang record-nya akan dihapus.
    """

    # Mengambil semua data dari database
    temp_seat_data = getAllData("temp_seat")

    # Menyaring data agar hanya menyisakan record yang BUKAN film ini
    temp_seat_data = {
        log_id: data
        for log_id, data in temp_seat_data.items()
        if data["judul_film"] != judul_film
    }

    updateData(temp_seat_data, "temp_seat")


# ------------------------------
# Nama fungsi: searchLogPemesananDuplicates
# Penjelasan fungsi : Mencari semua record pemesanan permanen yang
# cocok dengan nama customer dan judul film (untuk deteksi duplikat).
# ------------------------------
def searchTempLogPemesananDuplicates(nama: str, judul_film: str):
    """
    Mencari semua record pemesanan permanen berdasarkan nama dan judul film.

    Args:
        nama (str): Nama customer yang record-nya akan dihapus.
        judul_film (str): Judul film yang record-nya akan dihapus.

    Returns:
        dict: {log_id: data} dari semua record yang cocok.
              Dict kosong jika tidak ditemukan.
    """

    # Mengambil semua data dari database
    log_pemesanan_data = getAllData("temp_log_pemesanan")

    # Filter record berdasarkan nama dan judul film
    duplicates = {
        log_id: data
        for log_id, data in log_pemesanan_data.items()
        if data["nama"].lower() == nama.lower()
        and data["judul"].lower() == judul_film.lower()
    }

    return duplicates


# ------------------------------
# Nama fungsi: deleteLogPemesananByComposite
# Penjelasan fungsi : Menghapus SATU record pemesanan permanen dari
# log_pemesanan.txt berdasarkan composite key (nama + judul film +
# jumlah_tiket + nomor_kursi + date).
# ------------------------------
def deleteLogPemesananByComposite(
    nama: str,
    judul_film: str,
    jumlah_tiket: int = None,
    nomor_kursi: list = None,
):
    """
    Menghapus SATU record pemesanan permanen berdasarkan composite key.

    Args:
        nama (str): Nama customer yang record-nya akan dihapus.
        judul_film (str): Judul film untuk memastikan record yang tepat.
        jumlah_tiket (int, optional): Jumlah tiket yang dipesan.
        nomor_kursi (list, optional): Daftar nomor kursi yang dipesan.
    Returns:
        bool: True jika berhasil menghapus, False jika tidak ditemukan.
    """

    # Mengambil semua data dari database
    log_pemesanan_data = getAllData("log_pemesanan")

    # Cari record yang cocok
    target_log_id = None
    for log_id, data in log_pemesanan_data.items():
        if data["nama"].lower() != nama.lower():
            continue
        if data["judul"].lower() != judul_film.lower():
            continue

        # Cek jumlah_tiket jika disediakan
        if jumlah_tiket is not None:
            if str(data.get("jumlah_tiket")) != str(jumlah_tiket):
                continue

        # Cek nomor_kursi jika disediakan (strip spasi dan ignore urutan)
        if nomor_kursi is not None:
            data_kursi = data.get("nomor_kursi", [])
            kursi_normalized = [k.strip() for k in nomor_kursi if k and k.strip()]
            data_kursi_normalized = [k.strip() for k in data_kursi if k and k.strip()]
            if sorted(data_kursi_normalized) != sorted(kursi_normalized):
                continue

        # Jika sampai sini, record cocok
        target_log_id = log_id
        break

    # Jika tidak ditemukan, return False
    if not target_log_id:
        return False

    # Hapus SATU record yang ditemukan
    del log_pemesanan_data[target_log_id]

    updateData(log_pemesanan_data, "log_pemesanan")
    return True
