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
import os
import sys
import time

console = Console()


def _clear():
    os.system("cls" if sys.platform == "win32" else "clear")


def _processing(msg="Memproses"):
    _clear()
    symbols = ["|", "/", "-", "\\"]
    start = time.time()
    i = 0
    while time.time() - start < 3:
        print(f"\r{msg} {symbols[i % len(symbols)]}", end="", flush=True)
        time.sleep(0.15)
        i += 1
    _clear()


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

    return user_ticket, selected_seats


def resetOrder(queue, ticket):
    queue.front = None
    queue.rear = None
    queue.urutan = 1

    ticket.head = None
    ticket.tail = None
