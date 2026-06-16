# Antrean Tiket Bioskop | TPL2106 B | Algoritma Struktur Data

Aplikasi Command Line Interface (CLI) berbasis Python untuk mengelola pemesanan tiket bioskop oleh kasir tiket. Sistem ini mengimplementasikan Queue untuk memproses pesanan pelanggan secara pertama masuk pertama keluar, dan Linked List untuk mengelola data pemesanan secara efisien.

## Video & Laporan
- **Video:**
- **Laporan:** https://github.com/wilanta/ASD_B_4/blob/master/Laporan_Kelompok 4_TPL B_Antrean Tiket Bioskop.pdf

## Team & Role | Kelompok 4

- **J0403251040** M. Lutfi Ramadhan Warendra (Engineer, Advisor)
- **J0403251070** Fateeh Falah Hendarto (Engineer, Advisor, QA)
- **J0403251098** Wildhan Dzikrihantara (Project Manager, Engineer)

## Dependencies

- `inquirerpy` - untuk prompt CLI interaktif (`main.py`, `CRUD/operations/film.py`, `CRUD/operations/antrean.py`)
- `reportlab` - untuk membuat PDF struk dan laporan penjualan tiket (`CRUD/operations/invoice.py`, `CRUD/operations/report.py`)
- `rich` - untuk tampilan console yang terformat (`main.py`, `CRUD/operations/*`, `CRUD/utils/*`)

## Cara Menjalankan

1. Clone repository ini atau unduh file ZIP:

```bash
git clone https://github.com/wilanta/ASD_B_4.git
```

2. Masuk ke direktori proyek:

```bash
cd ASD_B_4-master
```

3. Buat virtual environment dan aktifkan:

```bash
python -m venv venv
```

- Windows:

```bash
venv\Scripts\activate
```

- Bash:

```bash
source venv/Scripts/activate
```

- macOS/Linux:

```bash
source venv/bin/activate
```

4. Instal dependensi yang dibutuhkan:

```bash
pip install -r requirements.txt
```

5. Jalankan aplikasi:

```bash
python main.py
```
