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

# Untuk interface
from InquirerPy import inquirer
from rich import print
import shutil


# ------------------------------
# Nama fungsi: main
# Penjelasan fungsi : Untuk tampilan dan kontrol main menu.
# ------------------------------
def main():
    # menampilkam menu utama secara berulang sampai user memilih untuk keluar
    while True:
        print("""
[bold white]
██████╗ ██╗ ██████╗ ███████╗██╗  ██╗ ██████╗ ██████╗      ██████╗ █████╗  ██████╗██████╗
██╔══██╗██║██╔═══██╗██╔════╝██║ ██╔╝██╔═══██╗██╔══██╗    ██╔════╝██╔══██╗██╔════╝██╔══██╗
██████╔╝██║██║   ██║███████╗█████╔╝ ██║   ██║██████╔╝    ██║     ███████║██║     ██████╔╝
██╔══██╗██║██║   ██║╚════██║██╔═██╗ ██║   ██║██╔═══╝     ██║     ██╔══██║██║     ██╔══██╗
██████╔╝██║╚██████╔╝███████║██║  ██╗╚██████╔╝██║         ╚██████╗██║  ██║╚██████╗██████╔╝
╚═════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝          ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═════╝
[/bold white]
""")
        width = shutil.get_terminal_size().columns
        print("-" * width)

        print("[bold white]Pilih menu yang ingin diakses[/bold white]")
        print("[dim]Pilih untuk melanjutkan.[/dim]\n")

        print("-" * width)

        # Menampilkan pilihan dan meminta pilihan dari user
        choice = inquirer.select(
            message="",
            choices=[
                "1. Sistem Informasi Antrean",
                "2. Daftar Film",
                "3. Tambah Film",
                "4. Laporan Penjualan Tiket",
                "0. Keluar",
            ],
            default="Auto (match terminal)",
            pointer=">",
            instruction="Gunakan ↑ ↓ untuk memindahkan opsi, Enter untuk memilih",
        ).execute()

        # Mengecek nilai dari variabel 'pilihan'
        match choice:
            case "1. Sistem Informasi Antrean":  # Sistem Antrean
                # Memanggil pilihFilm untuk memilih film yang akan dioperasikan antreannya
                film_id = pilihFilm()

                # Memanggil fungsi sistem antrean
                if film_id:
                    sistemAntrean(film_id)
                else:
                    print("Tidak sesuai nomor di urutan. Kembali ke menu utama...")

            case "2. Daftar Film":  # Show film
                film_id = pilihFilm()

                # Film_id validator
                if film_id is None:
                    continue

                choice = inquirer.select(
                    message="",
                    choices=[
                        "1. Update",
                        "2. Delete",
                        "0. Kembali",
                    ],
                    default="Auto (match terminal)",
                    pointer=">",
                    instruction="Gunakan ↑ ↓ untuk memindahkan opsi, Enter untuk memilih",
                ).execute()

                match choice:
                    case "1. Update":  # Update Film
                        film = getAllData("data_film").get(film_id)

                        # Title ubah film
                        print("\n======== Ubah Film ========")
                        print("Judul \t\t:", film["judul_film"])
                        print("Kuota Penonton \t:", film["kuota_penonton"])
                        print("\nKosongkan isian jika tidak ingin mengganti isi data")

                        # Input data film dan Loop hingga operasi selesai
                        while True:
                            judul = input("Judul \t\t: ").strip()
                            kuota_penonton = input("Kuota Penonton \t: ").strip()

                            # Validasi kuota penonton harus berupa angka
                            if not kuota_penonton or (
                                kuota_penonton.isdigit()
                                and 0 < int(kuota_penonton) <= 100
                            ):
                                break
                            print("Kuota penonton harus berupa angka valid!")

                        # Ubah data film di database
                        updateFilm(
                            judul_film=judul,
                            kuota_penonton=kuota_penonton,
                            film_id=film_id,
                        )

                        print("Film berhasil diubah!")

                    case "2. Delete":  # Delete Film
                        deleteFilm(film_id)

                        print("Film berhasil dihapus!")

                    case "0. Kembali":  # Kembali ke menu utama
                        print("Kembali ke menu utama.")
                        continue

                    case _:  # Pilihan tidak valid
                        print("Pilihan tidak valid!")

            case "3. Tambah Film":  # Tambah Film
                empty = True  # Flag untuk mengecek input kosong
                # Title tambah film
                print("\n======== Tambah Film ========")
                print("Kosongkan isian untuk membatalkan penambahan film\n")

                # Input data film dan Loop hingga operasi selesai
                while True:
                    judul = input("Judul \t\t: ").strip()
                    kuota_penonton = input("Kuota Penonton \t: ").strip()

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

            case "4. Laporan Penjualan Tiket":
                pass

            case "0. Keluar":  # Kembali ke menu utama
                print("Program dihentikan.")
                break

            case _:  # Pilihan tidak valid
                print("Pilihan tidak valid!\n")


# Untuk menjalankan fungsi main secara langsung
if __name__ == "__main__":
    main()
