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

# Antrean
from CRUD.operations.antrean import sistemAntrean

# film
from CRUD.operations.film import pilihFilm, addFilm, updateFilm, deleteFilm

from CRUD.utils.dataOps import getAllData


# ------------------------------
# Nama fungsi: main
# Penjelasan fungsi : Untuk tampilan dan kontrol main menu.
# ------------------------------
def main():
    # menampilkam menu utama secara berulang sampai user memilih untuk keluar
    while True:
        # Menampilkan pilihan
        print("\n==== BIOSKOP CACB ====")
        print("1. Sistem Informasi Antrean")
        print("2. Daftar Film")
        print("3. Tambah Film")
        print("0. Keluar")
        print()

        # Meminta masukan pilihan dari user
        pilihan = input("Pilih : ")

        # Mengecek nilai dari variabel 'pilihan'
        match pilihan:
            case "1":  # Sistem Antrean
                # Memanggil pilihFilm untuk memilih film yang akan dioperasikan antreannya
                film_id = pilihFilm()

                # Memanggil fungsi sistem antrean
                if film_id:
                    sistemAntrean(film_id)
                else:
                    print("Tidak sesuai nomor di urutan. Kembali ke menu utama...")

            case "2":  # Show film
                film_id = pilihFilm()

                # Film_id validator
                if film_id is None:
                    continue

                print("\nPilih Operasi : ")
                print("1. Update")
                print("2. Delete")
                print("0. Kembali")

                pilihan = input("\nPilih : ")

                match pilihan:
                    case "1":  # Update Film
                        film = getAllData("data_film").get(film_id)

                        # Title ubah film
                        print("==== Ubah Film ====")
                        print("Judul \t\t:", film['judul_film'])
                        print("Kuota Penonton \t:", film['kuota_penonton'])
                        print("Kosongkan isian jika tidak ingin mengganti isi data")

                        # Input data film dan Loop hingga operasi selesai
                        while True:
                            judul = input("Judul \t\t: ").strip()
                            kuota_penonton = input(
                                "Kuota Penonton \t: ").strip()

                            # Validasi kuota penonton harus berupa angka
                            if not kuota_penonton or (kuota_penonton.isdigit() and 0 < int(kuota_penonton) <= 100):
                                break
                            print("Kuota penonton harus berupa angka valid!")

                        # Ubah data film di database
                        updateFilm(
                            judul_film=judul,
                            kuota_penonton=kuota_penonton,
                            film_id=film_id,
                        )

                        print("Film berhasil diubah!")

                    case "2":  # Delete Film
                        deleteFilm(film_id)

                        print("Film berhasil dihapus!")

                    case "0":  # Kembali ke menu utama
                        print("Kembali ke menu utama.")
                        continue

                    case _:  # Pilihan tidak valid
                        print("Pilihan tidak valid!")

            case "3":  # Tambah Film
                empty = True  # Flag untuk mengecek input kosong
                # Title tambah film
                print("==== Tambah Film ====")
                print("Kosongkan isian untuk membatalkan penambahan film")

                # Input data film dan Loop hingga operasi selesai
                while True:
                    judul = input("Judul \t\t: ").strip()
                    kuota_penonton = input(
                        "Kuota Penonton \t: ").strip()

                    # Jika input kosong, aktifkan flag
                    if not judul and not kuota_penonton:
                        break
                    # Validasi kuota penonton harus berupa angka
                    if kuota_penonton.isdigit() and 0 < int(kuota_penonton) <= 100:
                        empty = not empty
                        break
                    print("Kuota penonton harus berupa angka valid!")

                # Jika tidak diberi input, batalkan penambahan film
                if empty:
                    print("Membatalkan penambahan film...")
                    continue

                # Tambahkan film baru ke database
                addFilm(judul, int(kuota_penonton))
                print("Film berhasil ditambah!")

            case "0":  # Kembali ke menu utama
                print("Program dihentikan.")
                break

            case _:  # Pilihan tidak valid
                print("Pilihan tidak valid!\n")


# Untuk menjalankan fungsi main secara langsung
if __name__ == "__main__":
    main()
