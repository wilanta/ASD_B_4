"""
==========================================================
Invoice
Mencetak struk pembayaran tiket bioskop dalam format PDF
secata otomatis setelah customer dilayani, lalu membuka
file PDF tersebut di browser.

Kontributor : M. Lutfi Ramadhan Warendra

Fungsi/fitur:
1. invoice - Membuat dan membuka file PDF struk pembayaran
==========================================================
"""

# Module and dependencies needs
from datetime import datetime
import webbrowser
import os
from reportlab.pdfgen import canvas

from CRUD.utils.seatSort import seat_sort


# ------------------------------
# Nama fungsi: invoice
# Penjelasan fungsi : Membuat dan membuka file PDF struk pembayaran tiket bioskop
# secara otomatis setelah customer dilayani.
# ------------------------------
def invoice(judul, nama, kursi):
    """
    Membuat invoice tiket bioskop dalam format PDF
    dan otomatis membuka file tersebut di browser.

    Args:
        judul (str): Judul film yang ditonton.
        nama (str): Nama customer.
        kursi (list): List nomor kursi yang dipesan.
    """

    # mengambil path direktori tempat file python ini berada
    base_dir = os.path.dirname(__file__)

    # menentukan folder penyimpanan invoice
    # path menjadi: CRUD/history/invoices
    folder = os.path.join(base_dir, "..", "history", "invoices")
    folder = os.path.abspath(folder)

    # membuat folder jika belum ada
    os.makedirs(folder, exist_ok=True)

    # membuat timestamp agar nama file selalu unik
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # menentukan nama file invoice
    filename = f"INV_{timestamp}.pdf"

    # menggabungkan folder dan nama file menjadi path lengkap
    filepath = os.path.join(folder, filename)

    # menentukan ukuran canvas seperti struk kasir (80mm)
    width = 226
    height = 300

    # membuat objek canvas PDF
    c = canvas.Canvas(filepath, pagesize=(width, height))

    # menentukan posisi awal penulisan teks (koordinat y)
    y = height - 30

    # jarak antar baris
    line_height = 15

    # menggunakan font monospace agar teks sejajar
    c.setFont("Courier", 10)

    # membuat data teks yang akan ditulis di struk
    data = [
        "BIOSKOP CACB",
        "Jalan Lodaya II, Bogor",
        "--------------------------------",
        f"Judul  : {judul}",
        f"Nama   : {nama}",
        f"Kursi  : {', '.join(seat_sort(kursi))}",
        f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "--------------------------------",
        "Dilayani : Admin",
        "",
        "Terima Kasih",
        "Silakan Datang Kembali",
    ]

    # loop untuk mencetak setiap baris teks ke PDF
    for line in data:
        # menulis teks pada koordinat tertentu
        c.drawString(10, y, line)

        # menurunkan posisi y agar baris berikutnya berada di bawah
        y -= line_height

    # menyimpan file PDF
    c.save()

    # mengubah path menjadi absolute path
    path = os.path.abspath(filepath)

    # membuka file PDF otomatis di browser
    webbrowser.open(f"file://{path}")

    # mengembalikan path file invoice
    return filepath
