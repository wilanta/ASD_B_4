"""
==========================================================
Manajemen Pemesanan Kursi
Memilih kursi yang tersedia untuk customer secara interaktif
dan menyimpan data pemesanan ke log.

Kontributor : Fateeh Falah Hendarto

Fungsi/fitur:
1. orderKursi    - Alur pemilihan kursi secara interaktif
2. display_seats - Menampilkan denah kursi bioskop di terminal
3. resetOrder    - Mengosongkan queue dan linked list
==========================================================
"""

from rich.console import Console
from rich.panel import Panel

# Utils
from CRUD.utils.clear import _clear

console = Console()


# ------------------------------
# Nama fungsi: display_seats
# Penjelasan fungsi : Menampilkan denah kursi bioskop di terminal.
# Kursi hijau menunjukkan tersedia, X merah menunjukkan terisi.
# ------------------------------
def display_seats(available_seats_list: list, total_seats: int):
    """
    Menampilkan layout kursi bioskop
    Hijau = tersedia
    Merah (X) = terisi

    Args:
        available_seats_list (list): List kursi yang masih tersedia.
        total_seats (int): Total kapasitas kursi (kuota_penonton) film.
                            Digunakan agar kursi yang sudah terisi tetap
                            tampil sebagai X, bukan hilang dari denah.
    """

    if not available_seats_list:
        print("Tidak ada data kursi.")
        return

    # Bangun list semua kursi (K1..Ktotal) untuk layout denah
    all_seats = [f"K{i}" for i in range(1, total_seats + 1)]

    # Tampilkan header layar bioskop
    console.print(
        Panel(
            "[bold white]LAYAR BIOSKOP[/bold white]",
            border_style="yellow",
            expand=True,
        )
    )

    # Iterasi 10 kursi per baris
    for i in range(0, len(all_seats), 10):
        row = []

        current_row = all_seats[i : i + 10]

        # Warnai kursi: hijau = tersedia, merah X = terisi
        for idx, seat in enumerate(current_row):
            if seat in available_seats_list:
                row.append(f"[green]{seat:<5}[/green]")
            else:
                row.append(f"[red]{'X':<5}[/red]")

            # Tambah spasi di tengah baris (lorong)
            if idx == 4:
                row.append(" " * 6)

        console.print(" ".join(row))


# ------------------------------
# Nama fungsi: orderKursi
# Penjelasan fungsi : Alur pemilihan kursi secara interaktif.
# Customer memilih kursi satu per satu berdasarkan jumlah tiket yang dipesan.
# ------------------------------
def orderKursi(user_ticket: int, available_seats_list: list, total_seats: int):
    """
    Mengelola pemilihan kursi secara interaktif.

    Args:
        user_ticket (int): Jumlah tiket yang dipesan customer.
        available_seats_list (list): List kursi yang masih tersedia.
        total_seats (int): Total kapasitas kursi (kuota_penonton) film.

    Returns:
        tuple: (jumlah tiket, list kursi yang dipilih, list kursi tersisa).
    """

    selected_seats = []

    # Loop sebanyak jumlah tiket yang dipesan
    for i in range(user_ticket):
        while True:
            _clear()

            # Tampilkan header pemilihan kursi
            console.print(
                Panel(
                    f"[bold cyan]Pilih Kursi Tiket ke-{i + 1}[/bold cyan]",
                    border_style="cyan",
                )
            )

            # Tampilkan denah kursi terkini
            display_seats(available_seats_list, total_seats)

            # Input kursi dari user (uppercase & strip)
            select = (
                input(f"\nMasukkan kursi tiket ke-{i + 1} (contoh: K12): ")
                .upper()
                .strip()
            )

            # Jika kursi valid dan tersedia, hapus dari list available & simpan
            if select in available_seats_list:
                available_seats_list.remove(select)
                selected_seats.append(select)
                break

            console.print("[bold red]Kursi tidak valid / sudah terpakai.[/bold red]")
            input("Tekan Enter untuk mencoba lagi...")

    # Kembalikan tiket, kursi yang dipilih, dan sisa kursi tersedia
    return user_ticket, selected_seats, available_seats_list


# ------------------------------
# Nama fungsi: resetOrder
# Penjelasan fungsi : Mengosongkan struktur antrean (queue dan ticket linked list).
# Digunakan saat mereset sesi antrean untuk film tertentu.
# ------------------------------
def resetOrder(queue, ticket):
    """Mengosongkan queue dan linked list ticket."""
    queue.front = None
    queue.rear = None
    queue.urutan = 1

    ticket.head = None
    ticket.tail = None
