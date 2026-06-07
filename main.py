"""
==========================================================
Main Menu
Titik masuk utama aplikasi BIOSKOP CACB.
Berisi navigasi menu dan kontrol ke seluruh fitur sistem.

Kontributor : Wildhan Dzikrihantara, M. Lutfi Ramadhan Warendra

Fungsi/fitur:
1. main - Menampilkan menu utama dan mengarahkan ke fitur yang dipilih
==========================================================
"""

# Import features yang akan digunakan di main

# Antrean
from CRUD.operations.antrean import sistemAntrean

# film
from CRUD.operations.film import pilihFilm, addFilm, updateFilm, deleteFilm

from CRUD.utils.dataOps import getAllData

# Report
from CRUD.operations.report import generateReport

# Untuk interface
from InquirerPy import inquirer
from rich import print
from CRUD.utils.clear import _clear
from CRUD.utils.loading import _processing
import shutil
from rich.console import Console

console = Console()


# ------------------------------
# Nama fungsi: main
# Penjelasan fungsi : Untuk tampilan dan kontrol main menu.
# ------------------------------
def main():
    while True:
        _clear()
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
        # Cetak garis pemisah sepanjang lebar terminal
        print("-" * width)

        print("[bold white]Pilih menu yang ingin diakses[/bold white]")
        print("[dim]Pilih untuk melanjutkan.[/dim]\n")

        # Cetak garis pemisah sebelum daftar pilihan
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

                # Validasi film_id dan panggil sistem antrean
                if film_id:
                    _clear()
                    sistemAntrean(film_id)
                else:
                    _clear()
                    print("Tidak sesuai nomor di urutan. Kembali ke menu utama...")

            case "2. Daftar Film":  # Show film
                _clear()
                film_id = pilihFilm()

                # Film_id validator
                if film_id is None:
                    continue

                # Tampilkan sub-menu untuk update atau delete film
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

                        # Tampilkan header form ubah film
                        console.print("\n[bold]Ubah Film[/bold]")
                        console.print("[dim]────────────────────────────────[/dim]\n")

                        # Tampilkan data film saat ini
                        console.print(
                            f"[cyan]Judul Film[/cyan]        : {film['judul_film']}"
                        )
                        console.print(
                            f"[cyan]Kuota Penonton[/cyan]   : {film['kuota_penonton']}"
                        )

                        console.print(
                            "\n[dim]Kosongkan isian jika tidak ingin mengganti data[/dim]\n"
                        )

                        # Input judul dan kuota baru dengan validasi
                        while True:
                            judul = console.input(
                                "[cyan]Judul Film Baru[/cyan]   : "
                            ).strip()

                            kuota_penonton = console.input(
                                "[cyan]Kuota Baru[/cyan]         : "
                            ).strip()

                            # Judul tidak boleh mengandung koma (delimiter CSV)
                            if "," in judul:
                                console.print(
                                    "\n[red]✗[/red] Judul film tidak boleh mengandung koma (,)\n"
                                )
                                continue

                            # Kuota boleh kosong atau angka 1-60
                            if not kuota_penonton or (
                                kuota_penonton.isdigit()
                                and 0 < int(kuota_penonton) <= 60
                            ):
                                break

                            console.print(
                                "\n[red]✗[/red] Kuota penonton harus berupa angka valid dan maksimal 60!\n"
                            )

                        _processing("Menyimpan perubahan...")

                        # Panggil updateFilm dengan nilai baru (atau kosong = keep)
                        updateFilm(
                            judul_film=judul,
                            kuota_penonton=kuota_penonton,
                            film_id=film_id,
                        )

                        _clear()

                        console.print("\n[green]✓[/green] Film berhasil diubah!\n")

                    case "2. Delete":  # Delete Film
                        _processing("Menghapus film...")
                        # Panggil deleteFilm untuk hapus dari database
                        deleteFilm(film_id)

                        _clear()
                        print("Film berhasil dihapus!")

                    case "0. Kembali":  # Kembali ke menu utama
                        _clear()
                        print("Kembali ke menu utama.")
                        continue

                    case _:  # Pilihan tidak valid
                        print("Pilihan tidak valid!")
                        continue

            case "3. Tambah Film":  # Tambah Film
                _clear()

                # Flag untuk menandai form kosong (batal tambah)
                empty = True

                # Tampilkan header form tambah film
                console.print("\n[bold]Tambah Film[/bold]")
                console.print("[dim]────────────────────────────────[/dim]")
                console.print(
                    "[dim]Kosongkan isian untuk membatalkan penambahan film[/dim]\n"
                )

                # Input judul & kuota dengan validasi
                while True:
                    judul = console.input("[cyan]Judul Film[/cyan]        \t: ").strip()
                    kuota_penonton = console.input(
                        "[cyan]Kuota Penonton[/cyan]   \t: "
                    ).strip()

                    # Jika salah satunya kosong, anggap user membatalkan
                    if not judul or not kuota_penonton:
                        break

                    # Judul tidak boleh mengandung koma (delimiter CSV)
                    if "," in judul:
                        console.print(
                            "\n[red]✗[/red] Judul film tidak boleh mengandung koma (,)\n"
                        )
                        continue

                    # Validasi kuota sebagai angka 1-60
                    if kuota_penonton.isdigit() and 0 < int(kuota_penonton) <= 60:
                        empty = False
                        break

                    console.print(
                        "\n[red]✗[/red] Kuota penonton harus berupa angka valid dan maksimal 60 orang!\n"
                    )

                # Jika form kosong, batalkan penambahan
                if empty:
                    console.print("\n[yellow]![/yellow] Membatalkan penambahan film...")
                    continue

                _processing("Menyimpan film...")

                # Tambah film ke database
                add_status = addFilm(judul, int(kuota_penonton))

                if not add_status:
                    console.print(
                        "[red]✗ Gagal menambahkan film[/red]: judul yang sama sudah terdaftar."
                    )
                    input("[Tekan enter untuk kembali]")

                _clear()

                console.print("\n[green]✓[/green] Film berhasil ditambahkan!\n")

            case "4. Laporan Penjualan Tiket":
                _clear()
                # Ambil data log_pemesanan permanent sebagai sumber laporan
                data = getAllData("log_pemesanan")

                # Jika belum ada data, tampilkan pesan dan kembali ke menu
                if not data:
                    print("Data log_pemesanan kosong!")
                    continue

                _processing("Membuat laporan...")
                # Generate laporan penjualan tiket
                generateReport(data)

                _clear()
                print("Laporan berhasil dibuat!")

            case "0. Keluar":  # Kembali ke menu utama
                _clear()
                print("Program dihentikan.")
                break

            case _:  # Pilihan tidak valid
                print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    main()
