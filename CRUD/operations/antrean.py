"""
==========================================================
Manajemen Sistem Antrean Pesanan Tiket Film.

Fungsi/fitur:
1. Masuk Antrean
2. Layani Antrean
3. Lihat Antrean
4. Lihat Data Pemesanan
5. Batalkan Antrean
6. Hapus Data Pemesanan
7. Cari Data Pemesanan
8. Reset Antrean dan Pemesanan
==========================================================
"""

# queue
from CRUD.operations.queue import Queue

# linked list / ticket
from CRUD.operations.ticket import Ticket

# order
from CRUD.operations.order import orderKursi, resetOrder

# invoice
from CRUD.operations.invoice import invoice

# utillities & libraries
from CRUD.utils.idGenerator import generateID
from CRUD.utils.dataOps import getAllData, searchData, updateData
from CRUD.utils.seatSort import seat_sort

# Untuk interface
from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer
from rich import print
import os
import sys
import time

# Clear screen helper
_clear = lambda: os.system("cls" if sys.platform == "win32" else "clear")

# Status messages for spinning display
_STATUS_MSGS = [
    "Mohon tunggu sebentar...",
    "Sedang memproses data...",
    "Hampir selesai...",
    "Memproses permintaan...",
]


# Spinner + ~3s delay helper using Rich Status
def _processing(msg="Memproses"):
    _clear()
    console = Console()
    with console.status(msg, spinner="dots") as status:
        start = time.time()
        i = 0
        while time.time() - start < 3:
            status.update(_STATUS_MSGS[i % len(_STATUS_MSGS)])
            time.sleep(0.75)
            i += 1
    _clear()


# ------------------------------
# Nama fungsi: sistemAntrean
# Penjelasan fungsi : Untuk memanage sistem antrian suatu film bioskop.
# ------------------------------


def _error(msg: str):
    _clear()
    console = Console()
    console.print(
        Panel(
            f"[bold red]{msg}[/bold red]",
            title="[bold red]Gagal[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
    )
    input("\n[Tekan Enter untuk kembali]")


def sistemAntrean(film_id: str):
    "Menu Sistem Antrean"

    _clear()

    # Mengambil data film dari database
    film_dict = searchData(film_id, "data_film")

    # Inisialisasi tiket dan kursi tersedia
    available_ticket = int(film_dict[film_id]["kuota_penonton"])
    available_seat = [
        "K" + str(i) for i in range(1, int(film_dict[film_id]["kuota_penonton"]) + 1)
    ]

    # Inisialisasi queue
    q = Queue()

    # Inisialisasi ticket
    ll = Ticket()

    # Menampilkan menu sistem antrean secara berulang sampai user memilih untuk kembali ke menu utama
    while True:
        # Menampilkan menu
        console = Console()

        judul = film_dict[film_id]["judul_film"]
        tiket = available_ticket

        content = f"""
        [bold white]Judul Film     :[/bold white] {judul}
        [bold white]Tiket Tersedia :[/bold white] {tiket}
        """

        print("\n\n\n")
        console.print(
            Panel(
                content,
                title="[bold yellow]BIOSKOP CACB[/bold yellow]",
                subtitle="[dim]Sistem Informasi Antrean[/dim]",
                border_style="yellow",
                padding=(1, 2),
            )
        )

        # Menampilkan pilihan dan meminta pilihan dari user
        print("\n[bold white]Pilih opsi[/bold white]")
        choice = inquirer.select(
            message="",
            choices=[
                "1. Masuk Antrean",
                "2. Layani Antrean",
                "3. Lihat Antrean",
                "4. Lihat Data Pemesanan",
                "5. Batalkan Antrean",
                "6. Hapus Data Pemesanan",
                "7. Cari Data Pemesanan",
                "8. Reset Antrean dan Pemesanan",
                "0. Kembali",
            ],
            default="Auto (match terminal)",
            pointer=">",
            instruction="Gunakan ↑ ↓ untuk memindahkan opsi, Enter untuk memilih",
        ).execute()

        # Mengecek nilai dari variabel 'pilih'
        match choice:
            case "1. Masuk Antrean":  # Masuk Antrean
                # Memeriksa ketersediaan tiket sebelum memasukan penonton ke antrean
                _clear()
                if available_ticket > 0:
                    empty = True

                    while True:
                        # Meminta nama penonton
                        nama_penonton = input(
                            "\nMasukkan nama penonton [Kosongkan isi dan enter untuk kembali]: "
                        ).strip()

                        # Jika nama penonton kosong, kembali ke menu
                        if not nama_penonton:
                            break

                        # Jika user memasukan inputan yang tidak tepat
                        if nama_penonton.strip().replace(" ", "").isalpha():
                            empty = not empty
                            break

                        print(
                            "Nama penonton harus berupa huruf dan tidak boleh berupa simbol."
                        )

                    if empty:
                        print("Antrean dibatalkan.")
                        continue

                    _processing("Menambahkan ke antrean...")
                    q.enqueue(nama_penonton)

                    _clear()
                    print(f"{nama_penonton} masuk antrean.")
                else:
                    print("Antrean Penuh, tiket habis!")

            case "2. Layani Antrean":  # Layani Antrean
                if q.isEmpty():
                    _error("Antrean kosong, tidak ada yang bisa dilayani!")
                    continue

                if available_ticket < 1:
                    _error("Tiket habis, tidak ada yang bisa dilayani!")
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

                _processing("Memproses pesanan...")
                _clear()

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

                # Mengambil data log pemesanan
                log_pemesanan = getAllData("log_pemesanan")

                # Memasukan data ke dict log_pemesanan untuk dimasukan ke field log_pemesanan
                log_pemesanan[generateID()] = {
                    "nama": nama_customer,
                    "jumlah_tiket": ticket_amount,
                    "urutan_antrean": urutan_antrean,
                    "judul": judul_film,
                    "date": q.front.create_at,
                }

                # Memasukan data ke field_log pemesanan
                updateData(data_dict=log_pemesanan, data_name="log_pemesanan")

                # Cetak invoice
                invoice(judul=judul_film, nama=nama_customer, kursi=selected_seat)

                # Hapus customer yang telah dilayani dari antrean
                served_node = q.dequeue()

                _clear()
                print(
                    f"\n[cyan]Invoice berhasil dicetak | {served_node.nama} telah dilayani![/cyan]\n"
                )

            case "3. Lihat Antrean":  # Lihat Antrean
                _clear()
                q.showQueue()
                input("[Tekan Enter untuk Kembali]")

            case "4. Lihat Data Pemesanan":  # Lihat Data Pemesanan
                _clear()
                ll.showTickets()
                input("[Tekan Enter untuk Kembali]")

            case "5. Batalkan Antrean":  # Batalkan Antrean
                if q.isEmpty():
                    _error("Antrean kosong, tidak ada data yang bisa dibatalkan!")
                    continue

                # Meminta inputan nama customer dari user
                while True:
                    nama = input(
                        "Nama customer yang akan dibatalkan (Enter untuk kembali): "
                    ).strip()

                    # Jika user memasukan inputan yang tidak tepat
                    if nama.strip().replace(" ", "").isalpha() or not nama:
                        break

                    print(
                        "Nama customer harus berupa huruf dan tidak boleh berupa simbol."
                    )

                if not nama:
                    print("Kembali ke menu...")
                    continue

                # Assign 2 value ke 2 variable.
                canceled_user, canceled_urutan = q.cancelQueue(nama)
                # Hapus customer dari antrean
                if not canceled_user:
                    _error("Nama tidak ditemukan.")
                    continue

                _clear()
                print(
                    f"Antrean atas nama {canceled_user}{f' dengan urutan {canceled_urutan}' if canceled_urutan else ''} berhasil dibatalkan."
                )

            case "6. Hapus Data Pemesanan":  # Hapus Data Pemesanan
                if ll.isEmpty():
                    _error("Data pemesanan kosong, tidak ada data yang bisa dibatalkan!")
                    continue

                while True:
                    # Meminta inputan nama customer dari user
                    nama = input(
                        "Nama customer yang akan dibatalkan [Enter untuk kembali]: "
                    ).strip()

                    if nama.isalpha() or not nama:
                        break

                    print(
                        "Nama customer harus berupa huruf dan tidak boleh berupa simbol."
                    )

                # Jika nama kosong, kembali ke menu
                if not nama:
                    print("Kembali ke menu...")
                    continue

                # Hapus customer dari node linked list data pemesanan dan field log_pemesanan
                _processing("Menghapus pemesanan...")
                refunded_ticket, refunded_seat = ll.deleteTicket(nama)

                # Cek apakah nama berada di list
                if refunded_ticket is None:
                    _error("Nama tidak ditemukan.")
                    continue

                # Tambahkan kembali tiket dan kursi tersedia
                available_ticket += refunded_ticket

                available_seat.extend(refunded_seat)
                available_seat = seat_sort(available_seat)

                _clear()
                print("Pemesanan berhasil dibatalkan!")

            case "7. Cari Data Pemesanan":  # Cari Data Pemesanan
                _clear()
                if ll.isEmpty():
                    _error("Data pemesanan kosong, tidak ada data yang bisa dicari!")
                    continue

                while True:
                    # Meminta inputan nama customer dari user
                    nama = input(
                        "Nama customer yang akan dicari (Enter untuk kembali): "
                    ).strip()

                    # Validasi input (Semua harus berisi huruf atau tidak menginputkan nama)
                    if nama.isalpha() or not nama:
                        break
                    print(
                        "Nama customer harus berupa huruf dan tidak boleh berupa simbol."
                    )

                # Jika nama kosong, kembali ke menu
                if not nama:
                    print("Kembali ke menu...")
                    continue

                # Cari data di node linked list pemesanan / ticket
                if not ll.searchTicket(nama):
                    _error("Nama tidak ditemukan.")

            case "8. Reset Antrean dan Pemesanan":  # Reset Antrean dan Pemesanan
                _processing("Mereset antrean...")
                # Call Function Reset
                resetOrder(queue=q, ticket=ll)

                # Reset available ticket dan available seat
                available_ticket = int(film_dict[film_id]["kuota_penonton"])
                available_seat = [
                    "K" + str(i)
                    for i in range(1, int(film_dict[film_id]["kuota_penonton"]) + 1)
                ]

                _clear()
                print("Antrean dan pemesanan berhasil di-reset.\n")

            case "0. Kembali":  # Kembali ke menu utama
                _clear()
                print("Kembali ke menu utama.")
                break

            case _:  # Invalid input
                print("Pilihan tidak valid!\n")
