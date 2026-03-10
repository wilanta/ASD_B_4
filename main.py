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
from CRUD.operations.queue import Queue

# linked list
from CRUD.operations.linkedList import LinkedList

# order
from CRUD.operations.order import orderKursi, resetOrder

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
    else:
        print("Nomor urut tidak valid.")
        return


# ------------------------------
# Nama fungsi: sistemAntrean
# Penjelasan fungsi : Untuk memanage sistem antrian suatu film bioskop.
# ------------------------------
def sistemAntrean(film_id: str):
    "Menu Sistem Antrean"

    # Mengambil data film dari database
    film_dict = searchData(film_id, "data_film")

    # Inisialisasi tiket dan kursi tersedia
    available_ticket = int(film_dict[film_id]["kuota_penonton"])
    available_seat = [
        "K" + str(i) for i in range(1, int(film_dict[film_id]["kuota_penonton"]) + 1)
    ]

    # Inisialisasi queue
    q = Queue()

    # Inisialisasi linked list
    ll = LinkedList()

    # Menampilkan menu sistem antrean secara berulang sampai user memilih untuk kembali ke menu utama
    while True:
        # Menampilkan menu
        print("====== Sistem Informasi Antrean ======")
        print(
            f"Judul Film \t: {film_dict[film_id]['judul_film']}\nTiket Tersedia \t: {available_ticket}\n"  # Menampilkan informasi film
        )

        # Menampilkan opsi
        print("1. Masuk Antrean")
        print("2. Layani Antrean")
        print("3. Lihat Antrean")
        print("4. Lihat Data Pemesanan")
        print("5. Batalkan Antrean")
        print("6. Hapus Data Pemesanan")
        print("7. Cari Data Pemesanan")
        print("8. Reset Antrean dan Pemesanan")
        print("0. Kembali")

        # Meminta masukan pilihan dari user
        pilih = input("\nPilih : ")

        # Mengecek nilai dari variabel 'pilih'
        match pilih:
            case "1":  # Masuk Antrean
                # Memeriksa ketersediaan tiket sebelum memasukan penonton ke antrean
                if available_ticket > 0:
                    # Meminta nama penonton
                    nama_penonton = input(
                        "Masukkan nama penonton (Enter untuk kembali): "
                    ).strip()

                    # Jika nama penonton kosong, kembali ke menu
                    if nama_penonton == "":
                        continue

                    # Jika user memasukan inputan yang tidak tepat
                    while (
                        not isinstance(nama_penonton, str)
                        or not nama_penonton.isalpha()
                    ):
                        print(
                            "Nama penonton harus berupa huruf dan tidak boleh berupa simbol."
                        )
                        nama_penonton = input("\nMasukkan nama penonton: ").strip()

                    # Menambahkan penonton ke antrean
                    q.enqueue(nama_penonton)

                    print(f"{nama_penonton} masuk antrean.")
                else:
                    print("Antrean Penuh, tiket habis!")

            case "2":  # Layani Antrean
                # Jika antrean kosong, maka tidak ada yang bisa dilayani
                if q.isEmpty():
                    print("Antrean kosong, tidak ada yang bisa dilayani!")
                    continue

                if available_ticket < 1:
                    print("Tiket habis, tidak ada yang bisa dilayani!")
                    continue

                # Menentukan jumlah max tiket yang bisa dipesan per customer
                max_kursi_per_cust = 4  # Constant

                # Loop user input
                while True:
                    try:
                        user_ticket = int(input("Masukkan jumlah tiket yang dipesan: "))

                        # Jika tiket kurang dari 1 atau lebih dari 4
                        if user_ticket < 1 or user_ticket > max_kursi_per_cust:
                            print("Hanya bisa memesan 1-4 tiket!")
                            continue

                        # Jika melebihi tiket yang tersedia
                        if user_ticket > available_ticket:
                            print(f"Hanya tersisa {available_ticket} tiket!")
                            continue

                        # Jika semua valid maka keluar loop
                        break

                    except ValueError:
                        print("Masukkan bilangan yang valid!")

                # Mengambil data jumlah_tiket dan nomor_kursi dari user
                ticket_amount, selected_seat = orderKursi(user_ticket, available_seat)

                # Kurangi tiket yang tersedia
                available_ticket -= ticket_amount

                # Update data di Node Queue
                q.updateQueue(
                    jumlah_tiket=ticket_amount,
                    nomor_kursi=selected_seat,
                    judul_film=film_dict[film_id]["judul_film"],
                )

                # Mengambil data untuk disalurkan ke Node Linked List dan log_pemesanan
                nama_customer = q.front.nama
                urutan_antrean = q.front.urutan_antrean
                judul_film = film_dict[film_id]["judul_film"]

                # Memasukan data ke Node Linked List
                ll.addTicket(
                    nama=nama_customer,
                    jumlah_tiket=ticket_amount,
                    nomor_kursi=selected_seat,
                    urutan_antrean=urutan_antrean,
                    judul_film=judul_film,
                )

                # Memasukan data ke dict untuk dimasukan ke field log_pemesanan
                data_dict = {
                    generateID(): {
                        "nama": nama_customer,
                        "jumlah_tiket": ticket_amount,
                        "urutan_antrean": urutan_antrean,
                        "judul": judul_film,
                        "date": q.front.create_at,
                    }
                }

                # Memasukan data ke field_log pemesanan
                updateData(data_dict=data_dict, data_name="log_pemesanan")

                # Hapus customer yang telah dilayani dari antrean
                served_node = q.dequeue()

                print(f"\n{served_node.nama} telah dilayani!\n")

            case "3":  # Lihat Antrean
                q.showQueue()

            case "4":  # Lihat Data Pemesanan
                ll.showTickets

            case "5":  # Batalkan Antrean
                # Jika antrean kosong, maka tidak ada data yang bisa dibatalkan
                if q.isEmpty():
                    print("Antrean kosong, tidak ada data yang bisa dibatalkan!")
                    continue

                # Meminta inputan nama customer dari user
                nama = input(
                    "Nama customer yang akan dibatalkan (Enter untuk kembali): "
                ).strip()

                # Jika nama kosong, kembali ke menu
                if nama == "":
                    continue

                # Jika user memasukan inputan yang tidak tepat
                while not isinstance(nama, str) or not nama.isalpha():
                    print(
                        "Nama customer harus berupa huruf dan tidak boleh berupa simbol."
                    )
                    nama = input("Nama customer yang akan dibatalkan : ").strip()

                # Hapus customer dari antrean
                q.cancelQueue(nama)

            case "6":  # Hapus Data Pemesanan
                # Jika data pemesanan kosong, maka tidak ada data yang bisa dibatalkan
                if ll.isEmpty():
                    print("Data pemesanan kosong, tidak ada data yang bisa dibatalkan!")
                    continue

                # Meminta inputan nama customer dari user
                nama = input(
                    "Nama customer yang akan dibatalkan (Enter untuk kembali): "
                ).strip()

                # Jika nama kosong, kembali ke menu
                if nama == "":
                    continue

                # Jika user memasukan inputan yang tidak tepat
                while not isinstance(nama, str) or not nama.isalpha():
                    print(
                        "Nama customer harus berupa huruf dan tidak boleh berupa simbol."
                    )
                    nama = input("Nama customer yang akan dibatalkan : ").strip()

                # Hapus customer dari node linked list data pemesanan dan field log_pemesanan
                ll.deleteTicket(nama)

                # Tambahkan kembali tiket tersedia
                available_ticket += 1

            case "7":  # Cari Data Pemesanan
                # Meminta inputan nama customer dari user
                nama = input(
                    "Nama customer yang akan dibatalkan (Enter untuk kembali): "
                ).strip()

                # Jika nama kosong, kembali ke menu
                if nama == "":
                    continue

                # Jika user memasukan inputan yang tidak tepat
                while not isinstance(nama, str) or not nama.isalpha():
                    print(
                        "Nama customer harus berupa huruf dan tidak boleh berupa simbol."
                    )
                    nama = input("Nama customer yang akan dibatalkan : ").strip()

                    # Cari data di node linked list pemesanan
                    ll.searchTicket(nama)

            case "8":  # Reset Antrean dan Pemesanan
                # Reset Antrean dan Pemesanan
                resetOrder()

            case "0":  # Kembali ke menu utama
                print("Kembali ke menu utama.")
                break

            case _:  # Invalid input
                print("Pilihan tidak valid!\n")


# ------------------------------
# Nama fungsi: main
# Penjelasan fungsi : Untuk tampilan dan kontrol main menu.
# ------------------------------
def main():
    # menampilkam menu utama secara berulang sampai user memilih untuk keluar
    while True:
        # Menampilkan pilihan
        print("==== BIOSKOP CACB ====")
        print("1. Sistem Informasi Antrean")
        print("2. Daftar Film")
        print("3. Tambah Film")
        print("0. Keluar")
        print()

        # Meminta masukan pilihan dari user
        pilihan = input("Pilih : ")

        # Mengecek nilai dari variabel 'pilihan'
        match pilihan:
            case "1":
                # Memanggil pilihFilm untuk memilih film yang akan dioperasikan antreannya
                film_id = pilihFilm()

                # Memanggil fungsi sistem antrean
                if film_id:
                    sistemAntrean(film_id)
                else:
                    print("=> Kembali ke menu utama.\n")
            case "2":
                # film_id = showFilm()

                print("\nPilih Operasi : ")
                print("1. Update")
                print("2. Delete")
                print("0. Kembali")

                pilihan = input("\nPilih : ")

                match pilihan:
                    case "1":
                        # updateFilm(film_id)
                        pass
                    case "2":
                        # deleteFilm(film_id)
                        pass
                    case "0":
                        print("Kembali ke menu utama.")
                        continue
                    case _:
                        print("Pilihan tidak valid!")
            case "3":
                addFilm()
            case "0":
                print("Program dihentikan.")
                break
            case _:
                print("Pilihan tidak valid!\n")


# Untuk menjalankan fungsi main secara langsung
if __name__ == "__main__":
    main()
