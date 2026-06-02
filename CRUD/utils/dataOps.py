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
        "log_pemesanan" -> {log_id: {'nama': ..., 'jumlah_tiket': ..., 'urutan_antrean': ..., 'judul': ..., 'date': ..., 'nomor_kursi': [...]}}
        "temp_log_pemesanan" -> {log_id: {'nama': ..., 'jumlah_tiket': ..., 'urutan_antrean': ..., 'judul': ..., 'date': ..., 'nomor_kursi': [...]}}
        "data_antrean" -> {film_id: {'urutan_counter': int, 'nodes': [Node dict list]}}
        "temp_seat" -> {film_id: {'judul_film': str, 'available_seat': [List kursi]}}
    """
    data = {}
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, f"../data/{data_name}.txt")
    file_path = os.path.abspath(file_path)

    try:
        # Baca file baris per baris dan parse sesuai data_name
        with open(file_path, "r", encoding="utf-8") as d:
            for row in d:
                row = row.strip()
                if not row:
                    continue
                list_row = row.split(",")

                # Parse khusus untuk data_antrean (format COUNTER & QUEUE)
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

                if data_name.lower() == "data_film":
                    # Parse baris data_film: film_id,judul,kuota
                    film_id, judul_film, kuota_penonton = list_row
                    data[film_id] = {
                        "judul_film": judul_film,
                        "kuota_penonton": kuota_penonton,
                    }
                elif data_name.lower() == "log_pemesanan":
                    # Validasi jumlah kolom minimal
                    if len(list_row) < 7:
                        print(
                            f"[warn] skipped malformed row in log_pemesanan: {row}"
                        )
                        continue

                    # Parse baris log_pemesanan
                    (
                        log_id,
                        nama,
                        jumlah_tiket,
                        urutan_antrean,
                        judul,
                        date,
                        nomor_kursi_raw,
                    ) = list_row[:7]

                    # Pisahkan nomor kursi berdasarkan delimiter "|"
                    nomor_kursi = (
                        [k for k in nomor_kursi_raw.split("|") if k]
                        if nomor_kursi_raw
                        else []
                    )

                    data[log_id] = {
                        "nama": nama,
                        "jumlah_tiket": jumlah_tiket,
                        "urutan_antrean": urutan_antrean,
                        "judul": judul,
                        "date": date,
                        "nomor_kursi": nomor_kursi,
                    }
                elif data_name.lower() == "temp_log_pemesanan":
                    if len(list_row) < 7:
                        print(
                            f"[warn] skipped malformed row in temp_log_pemesanan: {row}"
                        )
                        continue

                    (
                        log_id,
                        nama,
                        jumlah_tiket,
                        urutan_antrean,
                        judul,
                        date,
                        nomor_kursi_raw,
                    ) = list_row[:7]

                    nomor_kursi = (
                        [k for k in nomor_kursi_raw.split("|") if k]
                        if nomor_kursi_raw
                        else []
                    )

                    data[log_id] = {
                        "nama": nama,
                        "jumlah_tiket": jumlah_tiket,
                        "urutan_antrean": urutan_antrean,
                        "judul": judul,
                        "date": date,
                        "nomor_kursi": nomor_kursi,
                    }
                elif data_name.lower() == "temp_seat":
                    # Parse baris temp_seat: film_id,judul,k1,k2,...
                    film_id, judul_film, *available_seat = list_row
                    data[film_id] = {
                        "judul_film": judul_film,
                        "available_seat": available_seat,
                    }

    except FileNotFoundError:
        # Kembalikan dict kosong jika file belum ada
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
        "log_pemesanan" -> {log_id: {'nama': ..., 'jumlah_tiket': ..., 'urutan_antrean': ..., 'judul': ..., 'date': ..., 'nomor_kursi': [...]}}
        "temp_seat" -> {film_id: {'judul_film': str, 'available_seat': [List kursi]}}
    """

    data = getAllData(data_name)
    result = {}

    if target_id in data:
        # Susun ulang hasil berdasarkan tipe data
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
            nomor_kursi = data[target_id]["nomor_kursi"]
            result[target_id] = {
                "nama": nama,
                "jumlah_tiket": jumlah_tiket,
                "urutan_antrean": urutan_antrean,
                "judul": judul,
                "date": date,
                "nomor_kursi": nomor_kursi,
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
        # Tulis data_film: film_id,judul,kuota per baris
        if data_name.lower() == "data_film":
            with open(file_path, "w", encoding="utf-8") as d:
                for film_id in data_dict.keys():
                    judul_film = data_dict[film_id]["judul_film"]
                    kuota_penonton = data_dict[film_id]["kuota_penonton"]
                    d.write(f"{film_id},{judul_film},{kuota_penonton}\n")

        # log_pemesanan

        elif data_name.lower() == "log_pemesanan":
            # Tulis log permanent, gabung nomor kursi dengan "|"
            with open(file_path, "w", encoding="utf-8") as d:
                for log_id in data_dict.keys():
                    nama = data_dict[log_id]["nama"]
                    jumlah_tiket = data_dict[log_id]["jumlah_tiket"]
                    urutan_antrean = data_dict[log_id]["urutan_antrean"]
                    judul = data_dict[log_id]["judul"]
                    date = data_dict[log_id]["date"]
                    nomor_kursi = data_dict[log_id]["nomor_kursi"]

                    # Gabung list kursi jadi string dengan delimiter "|"
                    nomor_kursi_str = (
                        "|".join(nomor_kursi) if nomor_kursi else ""
                    )

                    row_field = ",".join(
                        [
                            str(log_id),
                            str(nama),
                            str(jumlah_tiket),
                            str(urutan_antrean),
                            str(judul),
                            str(date),
                            nomor_kursi_str,
                        ]
                    )
                    d.write(f"{row_field}\n")

        # temp_seat: film_id,judul,k1,k2,...
        elif data_name.lower() == "temp_seat":
            with open(file_path, "w", encoding="utf-8") as d:
                for film_id in data_dict.keys():
                    judul_film = data_dict[film_id]["judul_film"]
                    available_seat = data_dict[film_id]["available_seat"]

                    # Gabung film_id, judul dan semua kursi jadi satu baris
                    row_field = ",".join([film_id, judul_film] + available_seat)
                    d.write(f"{row_field}\n")

        # temp_log_pemesanan: format sama seperti log_pemesanan
        elif data_name.lower() == "temp_log_pemesanan":
            with open(file_path, "w", encoding="utf-8") as d:
                for log_id in data_dict.keys():
                    nama = data_dict[log_id]["nama"]
                    jumlah_tiket = data_dict[log_id]["jumlah_tiket"]
                    urutan_antrean = data_dict[log_id]["urutan_antrean"]
                    judul = data_dict[log_id]["judul"]
                    date = data_dict[log_id]["date"]
                    nomor_kursi = data_dict[log_id]["nomor_kursi"]

                    nomor_kursi_str = (
                        "|".join(nomor_kursi) if nomor_kursi else ""
                    )

                    row_field = ",".join(
                        [
                            str(log_id),
                            str(nama),
                            str(jumlah_tiket),
                            str(urutan_antrean),
                            str(judul),
                            str(date),
                            nomor_kursi_str,
                        ]
                    )
                    d.write(f"{row_field}\n")

        # data_antrean: tulis COUNTER per film dan QUEUE per node
        elif data_name.lower() == "data_antrean":
            with open(file_path, "w", encoding="utf-8") as d:
                for film_id, film_data in data_dict.items():
                    # Tulis counter urutan antrean
                    d.write(f"COUNTER,{film_id},{film_data.get('urutan_counter', 1)}\n")
                    # Tulis setiap node sebagai baris QUEUE
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
