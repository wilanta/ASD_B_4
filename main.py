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

                        console.print("\n[bold]Ubah Film[/bold]")
                        console.print("[dim]────────────────────────────────[/dim]\n")

                        console.print(
                            f"[cyan]Judul Film[/cyan]        : {film['judul_film']}"
                        )
                        console.print(
                            f"[cyan]Kuota Penonton[/cyan]   : {film['kuota_penonton']}"
                        )

                        console.print(
                            "\n[dim]Kosongkan isian jika tidak ingin mengganti data[/dim]\n"
                        )

                        while True:
                            judul = console.input(
                                "[cyan]Judul Film Baru[/cyan]   : "
                            ).strip()

                            kuota_penonton = console.input(
                                "[cyan]Kuota Baru[/cyan]         : "
                            ).strip()

                            if not kuota_penonton or (
                                kuota_penonton.isdigit()
                                and 0 < int(kuota_penonton) <= 60
                            ):
                                break

                            console.print(
                                "\n[red]✗[/red] Kuota penonton harus berupa angka valid dan maksimal 60!\n"
                            )

                        _processing("Menyimpan perubahan...")

                        updateFilm(
                            judul_film=judul,
                            kuota_penonton=kuota_penonton,
                            film_id=film_id,
                        )

                        _clear()

                        console.print("\n[green]✓[/green] Film berhasil diubah!\n")

                    case "2. Delete":  # Delete Film
                        _processing("Menghapus film...")
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

                empty = True

                console.print("\n[bold]Tambah Film[/bold]")
                console.print("[dim]────────────────────────────────[/dim]")
                console.print(
                    "[dim]Kosongkan isian untuk membatalkan penambahan film[/dim]\n"
                )

                while True:
                    judul = console.input("[cyan]Judul Film[/cyan]        \t: ").strip()
                    kuota_penonton = console.input(
                        "[cyan]Kuota Penonton[/cyan]   \t: "
                    ).strip()

                    if not judul and not kuota_penonton:
                        break

                    if kuota_penonton.isdigit() and 0 < int(kuota_penonton) <= 60:
                        empty = False
                        break

                    console.print(
                        "\n[red]✗[/red] Kuota penonton harus berupa angka valid dan maksimal 60 orang!\n"
                    )

                if empty:
                    console.print("\n[yellow]![/yellow] Membatalkan penambahan film...")
                    continue

                _processing("Menyimpan film...")

                addFilm(judul, int(kuota_penonton))

                _clear()

                console.print("\n[green]✓[/green] Film berhasil ditambahkan!\n")

            case "4. Laporan Penjualan Tiket":
                _clear()
                data = getAllData("log_pemesanan")

                if not data:
                    print("Data log_pemesanan kosong!")
                    continue

                _processing("Membuat laporan...")
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
