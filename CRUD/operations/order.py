"""
==========================================================
Manajemen Pemesanan Kursi & Manajemen Pemesanan Tiket
Untuk memilih kursi yang kosong untuk customer secara bebas
dan menyimpan pemesanan ke log_antrean.txt.

Kontributor : Fateeh Falah Hendarto
Fungsi/fitur:
1. orderKursi
2. resetOrder
==========================================================
"""

from rich.console import Console
from rich.panel import Panel

console = Console()


# ------------------------------
# Nama fungsi: display_seats
# Penjelasan fungsi : Untuk menampilkan seat yang tersedia.
# ------------------------------
def display_seats(available_seats_list: list, total_seats: int = 60):
    """
    Menampilkan layout kursi bioskop
    X = kursi terisi
    """

    all_seats = [f"K{i}" for i in range(1, total_seats + 1)]

    console.print(
        Panel(
            "[bold white]LAYAR BIOSKOP[/bold white]", border_style="yellow", expand=True
        )
    )

    for i in range(0, len(all_seats), 10):
        row = []

        for seat in all_seats[i : i + 10]:
            if seat in available_seats_list:
                row.append(f"[green]{seat:<5}[/green]")
            else:
                row.append(f"[red]{'X':<5}[/red]")

        console.print("".join(row))


# ------------------------------
# Nama fungsi: orderKursi
# Penjelasan fungsi : Untuk memilihkan kursi kosong untuk customer secara bebas.
# ------------------------------
def orderKursi(user_ticket: int, available_seats_list: list):
    """
    Order Kursi

    Args:
        user_ticket (int): Jumlah tiket customer
        available_seats_list (list): Kursi yang tersedia

    Returns:
        tuple: (jumlah tiket, kursi yang dipilih)
    """

    selected_seats = []

    for i in range(user_ticket):
        while True:
            console.clear()

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

    return user_ticket, selected_seats


# ------------------------------
# Nama fungsi: resetOrder
# Penjelasan fungsi : Untuk mereset sistem antrean menjadi 0 antrean kembali.
# ------------------------------
def resetOrder(queue, ticket):
    # reset queue
    queue.front = None
    queue.rear = None
    queue.urutan = 1

    # reset ticket
    ticket.head = None
    ticket.tail = None
