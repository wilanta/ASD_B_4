"""
==========================================================
Manajemen Sistem Antrean Pesanan Tiket Film.

Fungsi/fitur:
1. Masuk Antrean
2. Layani Antrean
3. Lihat Antrean
4. Lihat Data Pemesanan
5. Batalkan Antrean
6. Batalkan Pemesanan
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
from CRUD.utils.deleteTempSessions import (
    deleteTempPemesanan,
    deleteTempSeat,
    deleteLogPemesananByComposite,
    searchTempLogPemesananDuplicates,
)

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
        # Ambil counter urutan dan list node dari data film
        q.urutan = data[film_id].get("urutan_counter", 1)
        nodes = data[film_id].get("nodes", [])

        # Merekonstruksi linked list secara berurutan
        prev = None
        for node_dict in nodes:
            # Rekonstruksi node dari dictionary dengan fallback value
            node = Node(
                nama=node_dict["nama"],
                jumlah_tiket=node_dict.get("jumlah_tiket"),
                nomor_kursi=node_dict.get("nomor_kursi"),
                urutan_antrean=node_dict.get("urutan_antrean"),
                judul_film=node_dict.get("judul_film", judul_film),
            )
            node.create_at = node_dict.get("create_at", node.create_at)

            # Set front untuk node pertama, sambungkan node setelahnya
            if prev is None:
                q.front = node
            else:
                prev.next = node

            prev = node

        # Set rear ke node terakhir hasil rekonstruksi
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

    # Traversal queue dan konversi setiap node ke dict
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

    data[film_id] = {
        "urutan_counter": q.urutan,
        "nodes": nodes_list,
    }

    updateData(data, "data_antrean")


# ------------------------------
# Nama fungsi: _load_tickets
# Penjelasan fungsi : Memuat data pemesanan dari temp_log_pemesanan.txt
# ke linked list Ticket untuk film tertentu.
# ------------------------------
def _load_tickets(judul_film: str, ll: Ticket):
    """
    Memuat record pemesanan dari file ke linked list Ticket.

    Args:
        judul_film (str): Judul film sebagai kunci penyaringan record.
        ll (Ticket): Objek Ticket linked list sebagai target muat data.
    """

    log = getAllData("temp_log_pemesanan")

    # Iterasi semua record dan filter yang sesuai judul_film
    for cust_id, record in log.items():
        if record.get("judul") == judul_film:
            kursi_raw = record.get("nomor_kursi")

            # Normalisasi format nomor_kursi (bisa string dengan | atau list)
            if isinstance(kursi_raw, str):
                nomor_kursi = [k.strip() for k in kursi_raw.split("|") if k.strip()]

            elif isinstance(kursi_raw, list):
                nomor_kursi = kursi_raw

            else:
                nomor_kursi = []

            # Tambahkan ke linked list Ticket
            ll.addTicket(
                nama=record.get("nama", ""),
                jumlah_tiket=int(record.get("jumlah_tiket", 0)),
                nomor_kursi=nomor_kursi,
                urutan_antrean=int(record.get("urutan_antrean", 0)),
                judul_film=record.get("judul", judul_film),
                customer_id=cust_id,
            )


# ------------------------------
# Nama fungsi: _save_tickets
# Penjelasan fungsi : Menyimpan state Ticket linked list saat ini
# ke temp_log_pemesanan.txt (hanya records film ini).
# ------------------------------
def _save_tickets(judul_film: str, ll: Ticket):
    """
    Menyimpan state terbaru linked list Ticket
    ke temp_log_pemesanan tanpa menduplikasi data lama.

    Args:
        judul_film (str): Judul film.
        ll (Ticket): Objek linked list Ticket.
    """

    # Mengambil semua data lama
    temp_log = getAllData("temp_log_pemesanan")

    # Menghapus semua data film yang sama agar tidak duplikat saat re-save
    temp_log = {
        log_id: data
        for log_id, data in temp_log.items()
        if data.get("judul") != judul_film
    }

    # Traversal linked list
    current = ll.head

    while current is not None:
        # Menambahkan state terbaru ke temp_log
        temp_log[current.customer_id] = {
            "nama": current.nama,
            "jumlah_tiket": str(current.jumlah_tiket),
            "urutan_antrean": str(current.urutan_antrean),
            "judul": current.judul_film,
            "nomor_kursi": current.nomor_kursi,
            "date": str(current.create_at),
        }

        current = current.next

    # Simpan kembali ke file/database
    updateData(temp_log, "temp_log_pemesanan")


# ------------------------------
# Nama fungsi: _reconcile_seat_availability
# Penjelasan fungsi : Merekonsiliasi available_seat dengan data pemesanan
# yang ada di linked list Ticket untuk memastikan konsistensi.
# ------------------------------
def _reconcile_seat_availability(available_seat: list, ll: Ticket) -> list:
    """
    Merekonsiliasi daftar kursi tersedia dengan data pemesanan aktif.
    Menghapus kursi dari available_seat jika sudah dipesan di linked list.

    Args:
        available_seat (list): Daftar kursi yang tersedia.
        ll (Ticket): Linked list berisi data pemesanan aktif.

    Returns:
        list: Daftar kursi tersedia yang sudah direkonsiliasi.
    """
    # Kumpulkan semua kursi yang sudah dipesan dari linked list
    booked_seats = set()
    current = ll.head

    # Iterasi seluruh tiket dan kumpulkan kursi yang sudah dibooking
    while current is not None:
        if current.nomor_kursi:
            for seat in current.nomor_kursi:
                if seat and seat.strip():
                    booked_seats.add(seat.strip())
        current = current.next

    # Hapus kursi yang sudah dipesan dari available_seat
    reconciled_seats = [seat for seat in available_seat if seat not in booked_seats]

    return reconciled_seats


# ------------------------------
# Nama fungsi: sistemAntrean
# Penjelasan fungsi : Untuk memanage sistem antrian suatu film bioskop.
# ------------------------------
def sistemAntrean(film_id: str):
    """Menu Sistem Antrean"""

    film_dict = searchData(film_id, "data_film")

    # Load available seat
    temp_seat_data = searchData(film_id, "temp_seat")

    available_ticket: int
    available_seat: list

    current_kuota = int(film_dict[film_id]["kuota_penonton"])

    if temp_seat_data:
        # available seat loaded from database
        available_seat = list(temp_seat_data[film_id]["available_seat"])
        # available seat loaded from database
        available_seat = list(temp_seat_data[film_id]["available_seat"])

        # Rekonsiliasi dengan kuota terbaru agar perubahan kuota film
        # (melalui menu Daftar Film -> Update) terpropagasi ke temp_seat.
        # - Jika kuota naik: tambahkan kursi baru (K_max+1 .. K_new).
        # - Jika kuota turun: kursi dengan nomor di atas kuota baru
        #   dihapus dari daftar tersedia (kursi yang sudah terjual
        #   tetap aman karena sudah tidak ada di available_seat).
        existing_numbers = sorted(
            int(s[1:])
            for s in available_seat
            if isinstance(s, str) and s.startswith("K") and s[1:].isdigit()
        )
        max_existing = existing_numbers[-1] if existing_numbers else 0

        if max_existing < current_kuota:
            # Tambah kursi baru jika kuota dinaikkan
            available_seat.extend(
                "K" + str(i) for i in range(max_existing + 1, current_kuota + 1)
            )
        elif max_existing > current_kuota:
            # Hapus kursi dengan nomor di atas kuota baru
            available_seat = [s for s in available_seat if int(s[1:]) <= current_kuota]

        available_seat = seat_sort(available_seat)

    else:
        # create new available seat list and write to database
        available_seat = ["K" + str(i) for i in range(1, current_kuota + 1)]

    judul_film = film_dict[film_id]["judul_film"]

    # Load queue from file if exists
    q = _load_queue(film_id, judul_film)

    # Load booking/ticket data
    ll = Ticket()
    _load_tickets(judul_film, ll)

    # Rekonsiliasi available_seat dengan data pemesanan aktif
    # untuk memastikan kursi yang sudah dipesan tidak bisa dipilih lagi
    # (mencegah inkonsistensi data antar sesi)
    available_seat = _reconcile_seat_availability(available_seat, ll)
    available_ticket = len(available_seat)

    # Tulis hasil rekonsiliasi ke database agar persisten antar sesi
    temp_seat = getAllData("temp_seat")
    temp_seat[film_id] = {
        "judul_film": judul_film,
        "available_seat": available_seat,
    }
    updateData(data_dict=temp_seat, data_name="temp_seat")

    # Menu utama
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
                "6. Batalkan Pemesanan",
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
                        # Input nama penonton dengan validasi huruf
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

                    # Tambahkan customer ke antrean dan simpan state
                    q.enqueue(nama_penonton)

                    _save_queue(film_id, q)

                    _processing("Memproses...")
                    _clear()

                    print(f"[green]{nama_penonton} masuk antrean.[/green]")

                else:
                    print("[bold red]Antrean Penuh, tiket habis![/bold red]")

            case "2. Layani Antrean":
                # Validasi: antrean tidak boleh kosong
                if q.isEmpty():
                    _clear()

                    print(
                        "[bold red]Antrean kosong, tidak ada yang bisa dilayani![/bold red]"
                    )

                    input("\nTekan Enter untuk kembali...")
                    continue

                # Validasi: harus ada tiket tersedia
                if available_ticket < 1:
                    _clear()

                    print(
                        "[bold red]Tiket habis, tidak ada yang bisa dilayani![/bold red]"
                    )

                    input("\nTekan Enter untuk kembali...")
                    continue

                # Maksimum tiket yang boleh dipesan per customer
                max_kursi_per_cust = 4

                out = False
                while True:
                    try:
                        # Input jumlah tiket dengan validasi range
                        user_input = input(
                            "\nMasukkan jumlah tiket yang dipesan [Kosongkan isi dan enter untuk kembali]: "
                        ).strip()

                        if not user_input:
                            out = True
                            break

                        user_ticket = int(user_input)

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

                if out:
                    continue

                # Proses pemilihan kursi interaktif
                ticket_amount, selected_seat, available_seat = orderKursi(
                    user_ticket, available_seat, current_kuota
                )

                # Kurangi tiket tersedia
                available_ticket -= ticket_amount

                # remove selected_seat from database and write to database
                temp_seat = getAllData("temp_seat")

                temp_seat[film_id] = {
                    "judul_film": film_dict[film_id]["judul_film"],
                    "available_seat": available_seat,
                }

                updateData(data_dict=temp_seat, data_name="temp_seat")

                # Update data customer di front queue dengan tiket
                q.updateQueue(
                    jumlah_tiket=ticket_amount,
                    nomor_kursi=selected_seat,
                    judul_film=judul_film,
                )

                # Generate ID log baru untuk entri permanent
                log_id = generateID()

                # Ambil info customer yang sedang dilayani
                nama_customer = q.front.nama
                urutan_antrean = q.front.urutan_antrean

                # Tambahkan record ke linked list ticket
                ll.addTicket(
                    nama=nama_customer,
                    jumlah_tiket=ticket_amount,
                    nomor_kursi=selected_seat,
                    urutan_antrean=urutan_antrean,
                    judul_film=judul_film,
                    customer_id=log_id,
                )

                # save permanent log
                log_pemesanan = getAllData("log_pemesanan")

                log_pemesanan[log_id] = {
                    "nama": nama_customer,
                    "jumlah_tiket": ticket_amount,
                    "urutan_antrean": urutan_antrean,
                    "judul": judul_film,
                    "date": q.front.create_at,
                    "nomor_kursi": selected_seat,
                }

                # Simpan log permanent ke database
                updateData(data_dict=log_pemesanan, data_name="log_pemesanan")

                _processing("Memproses...")
                _clear()

                # Cetak invoice untuk customer
                invoice(judul=judul_film, nama=nama_customer, kursi=selected_seat)

                # Hapus customer dari front queue (sudah dilayani)
                served_node = q.dequeue()

                # Simpan state queue dan ticket terbaru
                _save_queue(film_id, q)
                _save_tickets(judul_film, ll)

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

                # Hapus customer dari antrean
                canceled_user, canceled_urutan = q.cancelQueue(nama)

                if not canceled_user:
                    print("[bold red]Nama tidak ditemukan.[/bold red]")

                    input("\nTekan Enter untuk kembali...")
                    continue

                _processing("Membatalkan antrean...")

                # Simpan state queue dan ticket setelah pembatalan
                _save_queue(film_id, q)
                _save_tickets(judul_film, ll)

                _clear()

                # Tampilkan pesan sukses dengan informasi urutan (jika ada)
                print(
                    f"[green]Antrean atas nama {canceled_user}{f' dengan urutan {canceled_urutan}' if canceled_urutan else ''} berhasil dibatalkan.[/green]"
                )

            case "6. Batalkan Pemesanan":
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

                    if nama.strip().replace(" ", "").isalpha() or not nama:
                        break

                    print(
                        "[bold red]Nama customer harus berupa huruf dan tidak boleh berupa simbol.[/bold red]"
                    )

                if not nama:
                    _clear()
                    print("Kembali ke menu...")
                    continue

                _processing("Mencari data pemesanan...")

                # Cek duplikat di log_pemesanan (juga sumber kebenaran untuk
                # nama+film+sesi karena data ini permanent dan lengkap)
                duplicates = searchTempLogPemesananDuplicates(nama, judul_film)

                # Tentukan jumlah_tiket & nomor_kursi yang akan dihapus
                # berdasarkan composite key
                target_jumlah_tiket = None
                target_nomor_kursi = None
                target_date = None

                if len(duplicates) > 1:
                    # Ada lebih dari 1 record dengan nama+film sama,
                    # minta user pilih (mengikuti pola cancelQueue)
                    print(
                        f"\nTerdapat {len(duplicates)} data dengan nama '{nama}' "
                        f"untuk film '{judul_film}':\n"
                    )

                    duplicate_list = list(duplicates.items())

                    for idx, (log_id, data) in enumerate(duplicate_list, start=1):
                        kursi_str = ", ".join(seat_sort(data.get("nomor_kursi", [])))
                        print(
                            f"{idx}. Jumlah tiket : {data.get('jumlah_tiket')}, "
                            f"kursi : {kursi_str}, "
                            f"tanggal : {data.get('date')}"
                        )

                    print("\n0. Kembali")

                    while True:
                        pilihan = input(
                            "\nPilih nomor data yang akan dibatalkan: "
                        ).strip()

                        if not pilihan:
                            _clear()
                            print("Kembali ke menu...")
                            break

                        try:
                            pilihan = int(pilihan)
                        except ValueError:
                            print("[bold red]Pilihan tidak valid![/bold red]")
                            continue

                        if pilihan == 0:
                            _clear()
                            print("Kembali ke menu...")
                            break

                        if 1 <= pilihan <= len(duplicate_list):
                            selected_log_id, selected_data = duplicate_list[pilihan - 1]
                            target_jumlah_tiket = int(
                                selected_data.get("jumlah_tiket", 0)
                            )
                            target_nomor_kursi = [
                                k.strip()
                                for k in selected_data.get("nomor_kursi", [])
                                if k and k.strip()
                            ]
                            target_date = selected_data.get("date")
                            break

                        print(
                            f"[bold red]Pilihan harus 0-{len(duplicate_list)}![/bold red]"
                        )

                    # Jika user membatalkan (input kosong / 0)
                    if target_jumlah_tiket is None:
                        continue

                elif len(duplicates) == 1:
                    # Tepat 1 record, gunakan composite key-nya
                    selected_data = list(duplicates.values())[0]
                    target_jumlah_tiket = int(selected_data.get("jumlah_tiket", 0))
                    target_nomor_kursi = [
                        k.strip()
                        for k in selected_data.get("nomor_kursi", [])
                        if k and k.strip()
                    ]
                    target_date = selected_data.get("date")
                else:
                    # Tidak ada di log_pemesanan (mungkin hanya di temp/tiket aktif)
                    # Tetap lanjut dengan None agar deleteTicketByComposite coba
                    # hapus berdasarkan nama saja
                    pass

                # Hapus dari linked list menggunakan composite key
                # (jika composite key tidak ada, fallback ke nama saja)
                if target_jumlah_tiket is not None and target_nomor_kursi is not None:
                    refunded_ticket, refunded_seat = ll.deleteTicketByComposite(
                        nama, target_jumlah_tiket, target_nomor_kursi
                    )
                else:
                    refunded_ticket, refunded_seat = ll.deleteTicket(nama)

                if refunded_ticket is None:
                    _clear()
                    print("[bold red]Nama tidak ditemukan.[/bold red]")
                    input("\nTekan Enter untuk kembali...")
                    continue

                # Kembalikan kuota tiket & kursi yang sudah dibatalkan
                available_ticket += refunded_ticket

                available_seat.extend(refunded_seat)

                available_seat = seat_sort(available_seat)

                # Rewrite temp_seat agar refund bersifat persisten
                # antar sesi
                temp_seat = getAllData("temp_seat")

                temp_seat[film_id] = {
                    "judul_film": judul_film,
                    "available_seat": available_seat,
                }

                updateData(data_dict=temp_seat, data_name="temp_seat")

                # Simpan state ticket terbaru
                _save_tickets(judul_film, ll)

                # Hapus juga dari log_pemesanan agar laporan akurat,
                # menggunakan composite key lengkap
                deleteLogPemesananByComposite(
                    nama=nama,
                    judul_film=judul_film,
                    jumlah_tiket=target_jumlah_tiket,
                    nomor_kursi=target_nomor_kursi,
                )

                _processing("Membatalkan pemesanan...")

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

                    if nama.strip().replace(" ", "").isalpha() or not nama:
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

                # delete seat data at temp_seat and reset seat availability
                deleteTempSeat(judul_film)
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
