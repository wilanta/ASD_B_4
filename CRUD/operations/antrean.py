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

# utilities & libraries
from CRUD.utils.idGenerator import generateID
from CRUD.utils.dataOps import getAllData, searchData, updateData
from CRUD.utils.seatSort import seat_sort
from CRUD.utils.node import Node
from CRUD.utils.clear import _clear
from CRUD.utils.loading import _processing

# Untuk interface
from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer
from rich import print


# ------------------------------
# Nama fungsi: _load_queue
# Penjelasan fungsi : Memuat state antrean dari file data_antrean.txt
# berdasarkan film_id yang diberikan.
# ------------------------------
def _load_queue(film_id: str, judul_film: str) -> Queue:
    """
    Memuat state antrean dari file untuk film tertentu.

    Args:
        film_id (str): ID film.
        judul_film (str): Judul film.

    Returns:
        Queue: Objek queue yang sudah dimuat dengan data dari file.
    """
    # Inisialisasi queue kosong
    q = Queue()
    data = getAllData("data_antrean")

    # Memuat nodes dari file jika sudah ada state tersimpan
    if film_id in data:
        q.urutan = data[film_id].get("urutan_counter", 1)
        nodes = data[film_id].get("nodes", [])

        # Merekonstruksi linked list secara berurutan
        prev = None
        for node_dict in nodes:
            node = Node(
                nama=node_dict["nama"],
                jumlah_tiket=node_dict.get("jumlah_tiket"),
                nomor_kursi=node_dict.get("nomor_kursi"),
                urutan_antrean=node_dict.get("urutan_antrean"),
                judul_film=node_dict.get("judul_film", judul_film),
            )
            node.create_at = node_dict.get("create_at", node.create_at)
            if prev is None:
                q.front = node
            else:
                prev.next = node
            prev = node

        q.rear = prev if prev else None

    return q


# ------------------------------
# Nama fungsi: _save_queue
# Penjelasan fungsi : Menyimpan state antrean saat ini ke file
# data_antrean.txt sesuai format dataOps.py.
# ------------------------------
def _save_queue(film_id: str, q: Queue):
    """
    Menyimpan state antrean saat ini ke file data_antrean.txt.

    Args:
        film_id (str): ID film.
        q (Queue): Objek queue yang state-nya akan disimpan.
    """
    # Mengumpulkan semua node menjadi list dictionary
    nodes_list = []
    current = q.front
    while current is not None:
        nodes_list.append(
            {
                "nama": current.nama,
                "jumlah_tiket": current.jumlah_tiket,
                "nomor_kursi": current.nomor_kursi,
                "urutan_antrean": current.urutan_antrean,
                "judul_film": current.judul_film,
                "create_at": current.create_at,
                "next": current.next.nama if current.next else None,
            }
        )
        current = current.next

    # Membaca data lama, menambahkan/memperbarui entry film ini, lalu menyimpan
    data = getAllData("data_antrean")
    data[film_id] = {"urutan_counter": q.urutan, "nodes": nodes_list}
    updateData(data, "data_antrean")


# ------------------------------
# Nama fungsi: _load_tickets
# Penjelasan fungsi : Untuk memuat data pemesanan dari log_pemesanan.txt ke linked list Ticket.
# ------------------------------
# Nama fungsi: _load_tickets
# Penjelasan fungsi : Memuat data pemesanan dari temp_log_pemesanan.txt
# ke linked list Ticket untuk film tertentu.
# ------------------------------
def _load_tickets(film_id: str, judul_film: str, ll: Ticket):
    """
    Memuat record pemesanan dari file ke linked list Ticket.

    Args:
        film_id (str): ID film (tidak digunakan langsung, digunakan judul_film untuk filter).
        judul_film (str): Judul film sebagai kunci penyaringan record.
        ll (Ticket): Objek Ticket linked list sebagai target muat data.
    """
    log = getAllData("temp_log_pemesanan")
    for record in log.values():
        if record.get("judul") == judul_film:
            kursi_raw = record.get("nomor_kursi")
            if isinstance(kursi_raw, str):
                nomor_kursi = [k.strip() for k in kursi_raw.split("|") if k.strip()]
            elif isinstance(kursi_raw, list):
                nomor_kursi = kursi_raw
            else:
                nomor_kursi = []
            ll.addTicket(
                nama=record.get("nama", ""),
                jumlah_tiket=int(record.get("jumlah_tiket", 0)),
                nomor_kursi=nomor_kursi,
                urutan_antrean=int(record.get("urutan_antrean", 0)),
                judul_film=record.get("judul", judul_film),
            )


# ------------------------------
# Nama fungsi: _save_tickets
# Penjelasan fungsi : Menyimpan state Ticket linked list saat ini
# ke temp_log_pemesanan.txt (hanya records film ini).
# ------------------------------
log_pemesanan_ID = generateID()


def _save_tickets(film_id: str, judul_film: str, ll: Ticket, restored_log: dict):
    """
    Menyimpan state Ticket linked list ke file temp_log_pemesanan.txt.

    Args:
        film_id (str): ID film.
        judul_film (str): Judul film sebagai filter record.
        ll (Ticket): Objek linked list Ticket yang akan disimpan.
        restored_log (dict): Log yang dibaca sebelumnya untuk disatukan.
    """
    # Mengumpulkan records dari linked list
    current = ll.head
    film_records = {}
    while current is not None:
        film_records[current.nama] = {
            "nama": current.nama,
            "jumlah_tiket": str(current.jumlah_tiket),
            "urutan_antrean": str(current.urutan_antrean),
            "judul": current.judul_film,
            "date": str(current.create_at),
        }
        current = current.next

    for log_id, record in restored_log.items():
        if record.get("judul") != judul_film:
            film_records[record.get("nama", "") + "_" + log_id] = {
                "nama": record.get("nama", ""),
                "jumlah_tiket": record.get("jumlah_tiket", ""),
                "urutan_antrean": record.get("urutan_antrean", ""),
                "judul": record.get("judul", ""),
                "date": record.get("date", ""),
            }

    result = {}
    for key, val in restored_log.items():
        if val.get("judul") == judul_film:
            continue
        result[key] = val

    for record in film_records.values():
        result[log_pemesanan_ID] = record

    updateData(result, "temp_log_pemesanan")


# ------------------------------
# Nama fungsi: deleteTempPemesanan
# Penjelasan fungsi : Menghapus semua record pemesanan sementara
# dari temp_log_pemesanan.txt berdasarkan judul film.
# ------------------------------
def deleteTempPemesanan(judul_film: str):
    """
    Menghapus record pemesanan sementara berdasarkan judul film.

    Args:
        judul_film (str): Judul film yang record-nya akan dihapus.
    """
    # Mengambil semua data dari database
    temp_pemesanan_data = getAllData("temp_log_pemesanan")

    # Menyaring data agar hanya menyisakan record yang BUKAN film ini
    # Record dengan judul yang cocok akan dihapus
    temp_pemesanan_data = {
        log_id: data
        for log_id, data in temp_pemesanan_data.items()
        if data["judul"] != judul_film
    }

    updateData(temp_pemesanan_data, "temp_log_pemesanan")


# ------------------------------
# Nama fungsi: sistemAntrean
# Penjelasan fungsi : Untuk memanage sistem antrian suatu film bioskop.
# ------------------------------
def sistemAntrean(film_id: str):
    """Menu Sistem Antrean"""

    film_dict = searchData(film_id, "data_film")
    available_ticket = int(film_dict[film_id]["kuota_penonton"])
    available_seat = [
        "K" + str(i) for i in range(1, int(film_dict[film_id]["kuota_penonton"]) + 1)
    ]

    judul_film = film_dict[film_id]["judul_film"]

    # Load queue from file if exists
    q = _load_queue(film_id, judul_film)

    # Load booking/ticket data from temp_log_pemesanan.txt
    restored_log = getAllData("temp_log_pemesanan")
    ll = Ticket()
    _load_tickets(film_id, judul_film, ll)

    # Menampilkan menu sistem antrean secara berulang sampai user memilih untuk kembali ke menu utama
    while True:
        console = Console()
        tiket = available_ticket
        content = f"""
        [bold white]Judul Film     :[/bold white] {judul_film}
        [bold white]Tiket Tersedia :[/bold white] {tiket}
        """

        _clear()
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

        match choice:
            case "1. Masuk Antrean":
                if available_ticket > 0:
                    empty = True

                    while True:
                        nama_penonton = input(
                            "\nMasukkan nama penonton [Kosongkan isi dan enter untuk kembali]: "
                        ).strip()

                        if not nama_penonton:
                            break

                        if nama_penonton.strip().replace(" ", "").isalpha():
                            empty = not empty
                            break

                        print(
                            "[bold red]Nama penonton harus berupa huruf dan tidak boleh berupa simbol.[/bold red]"
                        )

                    if empty:
                        _clear()
                        print("[bold red]Antrean dibatalkan.[/bold red]")
                        continue

                    q.enqueue(nama_penonton)
                    _save_queue(film_id, q)

                    _processing("Memproses...")
                    _clear()
                    print(f"[green]{nama_penonton} masuk antrean.[/green]")
                else:
                    print("[bold red]Antrean Penuh, tiket habis![/bold red]")

            case "2. Layani Antrean":
                if q.isEmpty():
                    _clear()
                    print(
                        "[bold red]Antrean kosong, tidak ada yang bisa dilayani![/bold red]"
                    )
                    input("\nTekan Enter untuk kembali...")
                    continue

                if available_ticket < 1:
                    _clear()
                    print(
                        "[bold red]Tiket habis, tidak ada yang bisa dilayani![/bold red]"
                    )
                    input("\nTekan Enter untuk kembali...")
                    continue

                max_kursi_per_cust = 4

                while True:
                    try:
                        user_ticket = int(input("Masukkan jumlah tiket yang dipesan: "))

                        if user_ticket < 1 or user_ticket > max_kursi_per_cust:
                            print("[bold red]Hanya bisa memesan 1-4 tiket![/bold red]")
                            continue

                        if user_ticket > available_ticket:
                            print(
                                f"[bold red]Hanya tersisa {available_ticket} tiket![/bold red]"
                            )
                            continue

                        break

                    except ValueError:
                        print("[bold red]Masukkan bilangan yang valid![/bold red]")

                ticket_amount, selected_seat = orderKursi(user_ticket, available_seat)

                available_ticket -= ticket_amount

                q.updateQueue(
                    jumlah_tiket=ticket_amount,
                    nomor_kursi=selected_seat,
                    judul_film=judul_film,
                )

                nama_customer = q.front.nama
                urutan_antrean = q.front.urutan_antrean

                ll.addTicket(
                    nama=nama_customer,
                    jumlah_tiket=ticket_amount,
                    nomor_kursi=selected_seat,
                    urutan_antrean=urutan_antrean,
                    judul_film=judul_film,
                )

                log_pemesanan = getAllData("log_pemesanan")
                log_pemesanan[log_pemesanan_ID] = {
                    "nama": nama_customer,
                    "jumlah_tiket": ticket_amount,
                    "urutan_antrean": urutan_antrean,
                    "judul": judul_film,
                    "date": q.front.create_at,
                }
                updateData(data_dict=log_pemesanan, data_name="log_pemesanan")

                _processing("Memproses...")
                _clear()
                invoice(judul=judul_film, nama=nama_customer, kursi=selected_seat)

                served_node = q.dequeue()
                _save_queue(film_id, q)
                _save_tickets(film_id, judul_film, ll, restored_log)

                print(
                    f"[cyan]Invoice berhasil dicetak | {served_node.nama} telah dilayani![/cyan]\n"
                )

            case "3. Lihat Antrean":
                _clear()
                q.showQueue()
                input("[Tekan Enter untuk Kembali]")

            case "4. Lihat Data Pemesanan":
                _clear()
                ll.showTickets()
                input("[Tekan Enter untuk Kembali]")

            case "5. Batalkan Antrean":
                _clear()
                if q.isEmpty():
                    print(
                        "[bold red]Antrean kosong, tidak ada data yang bisa dibatalkan![/bold red]"
                    )
                    input("\nTekan Enter untuk kembali...")
                    continue

                while True:
                    nama = input(
                        "Nama customer yang akan dibatalkan (Enter untuk kembali): "
                    ).strip()

                    if nama.strip().replace(" ", "").isalpha() or not nama:
                        break

                    print(
                        "[bold red]Nama customer harus berupa huruf dan tidak boleh berupa simbol.[/bold red]"
                    )

                if not nama:
                    _clear()
                    print("Kembali ke menu...")
                    continue

                canceled_user, canceled_urutan = q.cancelQueue(nama)

                if not canceled_user:
                    print("[bold red]Nama tidak ditemukan.[/bold red]")
                    input("\nTekan Enter untuk kembali...")
                    continue

                _processing("Membatalkan antrean...")
                _save_queue(film_id, q)
                _save_tickets(film_id, judul_film, ll, restored_log)

                _clear()
                print(
                    f"[green]Antrean atas nama {canceled_user}{f' dengan urutan {canceled_urutan}' if canceled_urutan else ''} berhasil dibatalkan.[/green]"
                )

            case "6. Hapus Data Pemesanan":
                _clear()
                if ll.isEmpty():
                    print(
                        "[bold red]Data pemesanan kosong, tidak ada data yang bisa dibatalkan![/bold red]"
                    )
                    input("\nTekan Enter untuk kembali...")
                    continue

                while True:
                    nama = input(
                        "Nama customer yang akan dibatalkan [Enter untuk kembali]: "
                    ).strip()

                    if nama.isalpha() or not nama:
                        break

                    print(
                        "[bold red]Nama customer harus berupa huruf dan tidak boleh berupa simbol.[/bold red]"
                    )

                if not nama:
                    _clear()
                    print("Kembali ke menu...")
                    continue

                _processing("Membatalkan pemesanan...")
                refunded_ticket, refunded_seat = ll.deleteTicket(nama)
                available_ticket += refunded_ticket
                available_seat.extend(refunded_seat)
                available_seat = seat_sort(available_seat)
                _save_tickets(film_id, judul_film, ll, restored_log)

                _clear()
                print("[green]Pemesanan berhasil dibatalkan![/green]")

            case "7. Cari Data Pemesanan":
                _clear()
                if ll.isEmpty():
                    print(
                        "[bold red]Data pemesanan kosong, tidak ada data yang bisa dicari![/bold red]"
                    )
                    input("\nTekan Enter untuk kembali...")
                    continue

                while True:
                    nama = input(
                        "Nama customer yang akan dicari (Enter untuk kembali): "
                    ).strip()

                    if nama.isalpha() or not nama:
                        break
                    print(
                        "[bold red]Nama customer harus berupa huruf dan tidak boleh berupa simbol.[/bold red]"
                    )

                if not nama:
                    _clear()
                    print("Kembali ke menu...")
                    continue

                _clear()
                if not ll.searchTicket(nama):
                    print("[bold red]Nama tidak ditemukan.[/bold red]")

                input("\nTekan Enter untuk kembali...")

            case "8. Reset Antrean dan Pemesanan":
                _processing("Mereset...")
                resetOrder(queue=q, ticket=ll)

                # Update available ticket and seat from film quota
                available_ticket = int(film_dict[film_id]["kuota_penonton"])
                available_seat = [
                    "K" + str(i)
                    for i in range(1, int(film_dict[film_id]["kuota_penonton"]) + 1)
                ]

                # Clear queue file for this film
                data = getAllData("data_antrean")
                if film_id in data:
                    del data[film_id]
                    updateData(data, "data_antrean")

                # Clear temp data pemesanan for this film
                deleteTempPemesanan(judul_film)

                _clear()
                print("[green]Antrean dan pemesanan berhasil di-reset.[/green]\n")

            case "0. Kembali":
                _clear()
                print("Kembali ke menu utama.")
                break

            case _:
                print("[bold red]Pilihan tidak valid![/bold red]\n")
