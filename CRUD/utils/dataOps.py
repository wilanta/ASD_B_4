"""
==========================================================
Data Operations
Berisi operations untuk mengelola data .txt

Fungsi/fitur:
1. getAllData
2. searchData
3. updateData
==========================================================
"""

# import libraries
import os

# ------------------------------
# Nama fungsi: getAllData
# Penjelasan fungsi : Mengembalikan seluruh isi data berupa dictionary.
# 
# Arguments : data_name (str) -> HANYA MENERIMA STRING BERUPA "data_film" ATAU "log_pemesanan".
# Returns : dict -> Semua row data.
# ------------------------------
def getAllData(data_name: str) -> dict:
    """
    Mengambil semua row data dari database
    
    Args:
        data_name (str): HANYA MENERIMA STRING BERUPA "data_film" ATAU "log_pemesanan"
    
    Returns:
        "data_film" -> {film_id: {'judul_film': ..., 'kuota_penonton': ...}}
        "log_pemesanan" -> {log_id: {'nama': ..., 'jumlah_tiket': ..., 'urutan_antrean': ..., 'judul': ..., 'date': ...}}
    """
    
    # Menampung data dari database
    data = {}
    
    # Mengambil dan menentukan path penyimpanan data
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, f"../data/{data_name}.txt")
    file_path = os.path.abspath(file_path)
    
    # Membuka file data berdasarkan data_name-nya untuk di-read
    try:
        with open(file_path, "r", encoding="utf-8") as d:
            # Menambah dari satu per satu dari database ke dictionary
            for row in d:
                # Bersihkan dari \n dan sisihkan data per field
                row = row.strip()
                list_row = row.split(",")
                
                # Lewati data yang tidak lengkap sesuai dengan panjang field database
                if (len(list_row) != 3 and data_name.lower() == "data_film") or (len(list_row) != 6 and data_name.lower() == "log_pemesanan"):
                    continue

                # Memilih database sesuai yang diinputkan pada parameter
                if data_name.lower() == "data_film": # Jika data_name:str berisi "data_film"
                    # Menyimpan pecahan data ke masing-masing variable
                    film_id, judul_film, kuota_penonton = list_row
                    
                    # Menambahkan satu per satu row data ke dictionary
                    data[film_id] = {
                        "judul_film": judul_film,
                        "kuota_penonton": kuota_penonton 
                    }
                elif data_name.lower() == "log_pemesanan": # Jika data_name:str berisi "log_pemesanan"
                    # Menyimpan pecahan data ke masing-masing variable
                    log_id, nama, jumlah_tiket, urutan_antrean, judul, date = list_row
                    
                    # Menambahkan satu per satu row data ke dictionary
                    data[log_id] = {
                        "nama": nama,
                        "jumlah_tiket": jumlah_tiket,
                        "urutan_antrean": urutan_antrean,
                        "judul": judul,
                        "date": date
                    }
                else:
                    return data
    
    # Error handling dan status ketika terjadi error saat pengambilan data
    except Exception as e:
        print(f"Gagal mengambil data | Error: {e}")
    
    return data


# ------------------------------
# Nama fungsi: searchData
# Penjelasan fungsi : Mengembalikan row data tunggal berdasarkan ID.
# 
# Arguments : 
# 1. target_id (str)
# 2. data_name (str)
# 
# Returns : dict -> row data tunggal berdasarkan ID.
# ------------------------------
def searchData(target_id: str, data_name: str) -> dict | None:
    """
    Mencari row data berdasarkan ID
    
    Args:
        target_id (str)
        data_name (str): HANYA MENERIMA STRING BERUPA "data_film" ATAU "log_pemesanan"
    
    Return:
        "data_film" -> {film_id: {'judul_film': ..., 'kuota_penonton': ...}}
        "log_pemesanan" -> {log_id: {'nama': ..., 'jumlah_tiket': ..., 'urutan_antrean': ..., 'judul': ..., 'date': ...}}
    """
    
    # Mengambil semua row data dari database
    data = getAllData(data_name)

    # Menampung hasil
    result = {}
    
    # Mencari ID dari database
    if target_id in data:
        # Memastikan database yang mana untuk pengembalian
        if data_name.lower() == "data_film":
            # Mengambil data dari ID yang terpilih
            judul_film = data[target_id]["judul_film"]
            kuota_penonton = data[target_id]["kuota_penonton"]
            
            # Memasukan data ke hasil untuk dikembalikan
            result[target_id] = {
                "judul_film": judul_film,
                "kuota_penonton": kuota_penonton
            }
        elif data_name.lower() == "log_pemesanan":
            # Mengambil data dari ID yang terpilih
            nama = data[target_id]["nama"]
            jumlah_tiket = data[target_id]["jumlah_tiket"]
            urutan_antrean = data[target_id]["urutan_antrean"]
            judul = data[target_id]["judul"]
            date = data[target_id]["date"]
            
            # Memasukan data ke hasil untuk dikembalikan
            result[target_id] = {
                "nama": nama,
                "jumlah_tiket": jumlah_tiket,
                "urutan_antrean": urutan_antrean,
                "judul": judul,
                "date": date,
            }
    else:
        return None
    
    return result


# ------------------------------
# Nama fungsi: updateData
# Penjelasan fungsi : Melakukan penyimpanan data ke database.
# 
# Arguments : 
# 1. data_dict (dict)
# 2. data_name (str)
# 
# Returns :
# ------------------------------
def updateData(data_dict: dict, data_name: str):
    """
    Menyimpan data ke database
    
    Args:
        data_dict (dict)
        data_name (str): HANYA MENERIMA STRING BERUPA "data_film" ATAU "log_pemesanan"
    
    Returns : 
    """
    
    # Memastikan data_name benar
    if data_name.lower() not in ["data_film", "log_pemesanan"]:
        raise ValueError("HANYA BOLEH DIISI DENGAN 'data_film' ATAU 'log_pemesanan'")
    
    # Mengambil dan menentukan path penyimpanan data
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, f"../data/{data_name}.txt")
    file_path = os.path.abspath(file_path)
    
    # Memasukan data dari dict ke database
    try:
        # Memastikan dalam database yang tepat
        if data_name.lower() == "data_film":
            with open(file_path, "w", encoding="utf-8") as d:
                for film_id in data_dict.keys():
                    # Menyimpan data dari dictionary untuk disimpan ke database
                    judul_film = data_dict[film_id]["judul_film"]
                    kuota_penonton = data_dict[film_id]["kuota_penonton"]
                    
                    # Menambahkan data ke database
                    d.write(f"{film_id},{judul_film},{kuota_penonton}\n")
        elif data_name.lower() == "log_pemesanan":
            with open(file_path, "w", encoding="utf-8") as d:
                for log_id in data_dict.keys():
                    # Menyimpan data dari dictionary untuk disimpan ke database
                    nama = data_dict[log_id]["nama"]
                    jumlah_tiket = data_dict[log_id]["jumlah_tiket"]
                    urutan_antrean = data_dict[log_id]["urutan_antrean"]
                    judul = data_dict[log_id]["judul"]
                    date = data_dict[log_id]["date"]
                    
                    # Menambahkan data ke database
                    d.write(f"{log_id},{nama},{jumlah_tiket},{urutan_antrean},{judul},{date}\n")
    
    except Exception as e:
        print(f"Gagal mengambil data | Error: {e}")