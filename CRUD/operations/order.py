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
def display_seats(available_seats_list: list):
    """
    Menampilkan layout kursi bioskop
    Hijau = tersedia
    Merah (X) = terisi
    """

    if not available_seats_list:
        print("Tidak ada data kursi.")
        return

    max_seat = max(int(seat[1:]) for seat in available_seats_list)

    all_seats = [f"K{i}" for i in range(1, max_seat + 1)]

    console.print(
        Panel(
            "[bold white]LAYAR BIOSKOP[/bold white]",
            border_style="yellow",
            expand=True,
        )
    )

    for i in range(0, len(all_seats), 10):
        row = []

        current_row = all_seats[i : i + 10]

        for idx, seat in enumerate(current_row):
            if seat in available_seats_list:
                row.append(f"[green]{seat:<5}[/green]")
            else:
                row.append(f"[red]{'X':<5}[/red]")

            if idx == 4:
                row.append(" " * 6)

        console.print(" ".join(row))


# ------------------------------
# Nama fungsi: orderKursi
# Penjelasan fungsi : Alur pemilihan kursi secara interaktif.
# Customer memilih kursi satu per satu berdasarkan jumlah tiket yang dipesan.
# ------------------------------
def orderKursi(user_ticket: int, available_seats_list: list):
    """
    Mengelola pemilihan kursi secara interaktif.

    Args:
        user_ticket (int): Jumlah tiket yang dipesan customer.
        available_seats_list (list): List kursi yang masih tersedia.

    Returns:
        tuple: (jumlah tiket, list kursi yang dipilih, list kursi tersisa).
    """

    selected_seats = []

    for i in range(user_ticket):
        while True:
            _clear()

            console.print(
                Panel(
                    f"[bold cyan]Pilih Kursi Tiket ke-{i + 1}[/bold cyan]",
                    border_style="cyan",
                )
            )

            display_seats(available_seats_list)

            select = (
                input(f"\nMasukkan kursi tiket ke-{i + 1} (contoh: K12): ")
                .upper()
                .strip()
            )

            if select in available_seats_list:
                available_seats_list.remove(select)
                selected_seats.append(select)
                break

            console.print("[bold red]Kursi tidak valid / sudah terpakai.[/bold red]")
            input("Tekan Enter untuk mencoba lagi...")

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
