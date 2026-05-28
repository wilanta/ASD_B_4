from CRUD.utils.dataOps import getAllData, updateData


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
