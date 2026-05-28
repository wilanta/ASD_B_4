"""
==========================================================
Data Operations
Mengelola operasi baca dan tulis data ke file .txt
sebagai database sederhana aplikasi bioskop.

Fungsi/fitur:
1. getAllData   - Membaca semua data dari file .txt
2. searchData   - Mencari satu baris data berdasarkan ID
3. updateData   - Menyimpan data dictionary ke file .txt
==========================================================
"""

import os


def getAllData(data_name: str) -> dict:
    """
    Mengambil semua row data dari database

    Args:
        data_name (str): HANYA MENERIMA STRING BERUPA "data_film", "log_pemesanan", "data_antrean", "temp_seat", ATAU "temp_log_pemesanan"

    Returns:
        "data_film" -> {film_id: {'judul_film': ..., 'kuota_penonton': ...}}
        "log_pemesanan" -> {log_id: {'nama': ..., 'jumlah_tiket': ..., 'urutan_antrean': ..., 'judul': ..., 'date': ...}}
        "temp_log_pemesanan" -> {log_id: {'nama': ..., 'jumlah_tiket': ..., 'urutan_antrean': ..., 'judul': ..., 'date': ...}}
        "data_antrean" -> {film_id: {'urutan_counter': int, 'nodes': [Node dict list]}}
        "temp_seat" -> {film_id: {'judul_film': str, 'available_seat': [List kursi]}}
    """
    data = {}
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, f"../data/{data_name}.txt")
    file_path = os.path.abspath(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as d:
            for row in d:
                row = row.strip()
                if not row:
                    continue
                list_row = row.split(",")

                if data_name.lower() == "data_antrean":
                    if list_row[0] == "COUNTER":
                        film_id = list_row[1]
                        counter = int(list_row[2])
                        if film_id not in data:
                            data[film_id] = {"urutan_counter": counter, "nodes": []}
                        else:
                            data[film_id]["urutan_counter"] = counter
                    elif list_row[0] == "QUEUE":
                        film_id = list_row[1]
                        nama = list_row[2]
                        jumlah_tiket = list_row[3] if list_row[3] != "" else None
                        nomor_kursi = (
                            list_row[4].split("|") if list_row[4] != "" else None
                        )
                        urutan_antrean = int(list_row[5])
                        judul_film = list_row[6]
                        date = list_row[7]
                        next_nama = (
                            list_row[8]
                            if len(list_row) > 8 and list_row[8] != ""
                            else None
                        )
                        node = {
                            "nama": nama,
                            "jumlah_tiket": jumlah_tiket,
                            "nomor_kursi": nomor_kursi,
                            "urutan_antrean": urutan_antrean,
                            "judul_film": judul_film,
                            "create_at": date,
                            "next": next_nama,
                        }
                        if film_id not in data:
                            data[film_id] = {"urutan_counter": 1, "nodes": []}
                        data[film_id]["nodes"].append(node)
                    continue

                if (len(list_row) != 3 and data_name.lower() == "data_film") or (
                    len(list_row) != 6 and data_name.lower() == "log_pemesanan"
                ):
                    continue

                if data_name.lower() == "data_film":
                    film_id, judul_film, kuota_penonton = list_row
                    data[film_id] = {
                        "judul_film": judul_film,
                        "kuota_penonton": kuota_penonton,
                    }
                elif data_name.lower() == "log_pemesanan":
                    log_id, nama, jumlah_tiket, urutan_antrean, judul, date = list_row
                    data[log_id] = {
                        "nama": nama,
                        "jumlah_tiket": jumlah_tiket,
                        "urutan_antrean": urutan_antrean,
                        "judul": judul,
                        "date": date,
                    }
                elif data_name.lower() == "temp_log_pemesanan":
                    log_id, nama, jumlah_tiket, urutan_antrean, judul, date = list_row
                    data[log_id] = {
                        "nama": nama,
                        "jumlah_tiket": jumlah_tiket,
                        "urutan_antrean": urutan_antrean,
                        "judul": judul,
                        "date": date,
                    }
                elif data_name.lower() == "temp_seat":
                    film_id, judul_film, *available_seat = list_row
                    data[film_id] = {
                        "judul_film": judul_film,
                        "available_seat": available_seat,
                    }

    except FileNotFoundError:
        return data
    except Exception as e:
        print(f"Gagal mengambil data | Error: {e}")

    return data


def searchData(target_id: str, data_name: str) -> dict | None:
    """
    Mencari row data berdasarkan ID

    Args:
        target_id (str)
        data_name (str): HANYA MENERIMA STRING BERUPA "data_film", "log_pemesanan", ATAU "temp_seat"

    Return:
        "data_film" -> {film_id: {'judul_film': ..., 'kuota_penonton': ...}}
        "log_pemesanan" -> {log_id: {'nama': ..., 'jumlah_tiket': ..., 'urutan_antrean': ..., 'judul': ..., 'date': ...}}
        "temp_seat" -> {film_id: {'judul_film': str, 'available_seat': [List kursi]}}
    """

    data = getAllData(data_name)
    result = {}

    if target_id in data:
        if data_name.lower() == "data_film":
            judul_film = data[target_id]["judul_film"]
            kuota_penonton = data[target_id]["kuota_penonton"]
            result[target_id] = {
                "judul_film": judul_film,
                "kuota_penonton": kuota_penonton,
            }
        elif data_name.lower() == "log_pemesanan":
            nama = data[target_id]["nama"]
            jumlah_tiket = data[target_id]["jumlah_tiket"]
            urutan_antrean = data[target_id]["urutan_antrean"]
            judul = data[target_id]["judul"]
            date = data[target_id]["date"]
            result[target_id] = {
                "nama": nama,
                "jumlah_tiket": jumlah_tiket,
                "urutan_antrean": urutan_antrean,
                "judul": judul,
                "date": date,
            }
        elif data_name.lower() == "temp_seat":
            judul_film = data[target_id]["judul_film"]
            available_seat = data[target_id]["available_seat"]
            result[target_id] = {
                "judul_film": judul_film,
                "available_seat": available_seat,
            }
    else:
        return None

    return result


def updateData(data_dict: dict, data_name: str):
    """
    Menyimpan data ke database

    Args:
        data_dict (dict)
        data_name (str): HANYA MENERIMA STRING BERUPA "data_film", "log_pemesanan", "data_antrean", 'temp_seat', ATAU "temp_log_pemesanan"

    Returns :
    """

    if data_name.lower() not in [
        "data_film",
        "log_pemesanan",
        "data_antrean",
        "temp_log_pemesanan",
        "temp_seat",
    ]:
        raise ValueError(
            "HANYA BOLEH DIISI DENGAN 'data_film', 'log_pemesanan', 'data_antrean', 'temp_seat', ATAU 'temp_log_pemesanan'"
        )

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, f"../data/{data_name}.txt")
    file_path = os.path.abspath(file_path)

    try:
        if data_name.lower() == "data_film":
            with open(file_path, "w", encoding="utf-8") as d:
                for film_id in data_dict.keys():
                    judul_film = data_dict[film_id]["judul_film"]
                    kuota_penonton = data_dict[film_id]["kuota_penonton"]
                    d.write(f"{film_id},{judul_film},{kuota_penonton}\n")
        elif data_name.lower() == "log_pemesanan":
            with open(file_path, "w", encoding="utf-8") as d:
                for log_id in data_dict.keys():
                    nama = data_dict[log_id]["nama"]
                    jumlah_tiket = data_dict[log_id]["jumlah_tiket"]
                    urutan_antrean = data_dict[log_id]["urutan_antrean"]
                    judul = data_dict[log_id]["judul"]
                    date = data_dict[log_id]["date"]
                    d.write(
                        f"{log_id},{nama},{jumlah_tiket},{urutan_antrean},{judul},{date}\n"
                    )
        elif data_name.lower() == "temp_seat":
            with open(file_path, "w", encoding="utf-8") as d:
                for film_id in data_dict.keys():
                    judul_film = data_dict[film_id]["judul_film"]
                    available_seat = data_dict[film_id]["available_seat"]

                    row_field = ",".join([film_id, judul_film] + available_seat)
                    print("helo world dajinduabdyuadgauv bway")
                    d.write(f"{row_field}\n")
        elif data_name.lower() == "temp_log_pemesanan":
            with open(file_path, "w", encoding="utf-8") as d:
                for log_id in data_dict.keys():
                    nama = data_dict[log_id]["nama"]
                    jumlah_tiket = data_dict[log_id]["jumlah_tiket"]
                    urutan_antrean = data_dict[log_id]["urutan_antrean"]
                    judul = data_dict[log_id]["judul"]
                    date = data_dict[log_id]["date"]
                    d.write(
                        f"{log_id},{nama},{jumlah_tiket},{urutan_antrean},{judul},{date}\n"
                    )
        elif data_name.lower() == "data_antrean":
            with open(file_path, "w", encoding="utf-8") as d:
                for film_id, film_data in data_dict.items():
                    d.write(f"COUNTER,{film_id},{film_data.get('urutan_counter', 1)}\n")
                    for node in film_data.get("nodes", []):
                        nomor_kursi_str = (
                            "|".join(node["nomor_kursi"]) if node["nomor_kursi"] else ""
                        )
                        next_nama = node["next"] if node.get("next") else ""
                        d.write(
                            f"QUEUE,{film_id},{node['nama']},{node.get('jumlah_tiket', '')},"
                            f"{nomor_kursi_str},{node['urutan_antrean']},"
                            f"{node['judul_film']},{node['create_at']},{next_nama}\n"
                        )

    except Exception as e:
        print(f"Gagal mengambil data | Error: {e}")
