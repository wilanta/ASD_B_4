from collections import Counter
from datetime import datetime
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def analyze(transaction_data):
    """
    Menganalisis data transaksi penjualan tiket.

    Parameters:
        transaction_data (dict):
            Dictionary berisi seluruh data transaksi.

    Returns:
        dict:
            Hasil analisis penjualan.
    """
    total_transactions = len(transaction_data)
    total_tickets_sold = 0

    movie_sales_counter = Counter()
    customer_transaction_counter = Counter()
    transaction_date_counter = Counter()

    for _, transaction in transaction_data.items():
        ticket_count = int(transaction["jumlah_tiket"])
        customer_name = transaction["nama"]
        movie_title = transaction["judul"]
        transaction_date = transaction["date"].split(" - ")[0]

        total_tickets_sold += ticket_count
        movie_sales_counter[movie_title] += ticket_count
        customer_transaction_counter[customer_name] += 1
        transaction_date_counter[transaction_date] += 1

    return {
        "total_transactions": total_transactions,
        "total_tickets_sold": total_tickets_sold,
        "best_selling_movie": movie_sales_counter.most_common(1)[0],
        "most_active_customer": customer_transaction_counter.most_common(1)[0],
        "busiest_day": transaction_date_counter.most_common(1)[0],
    }


def generateReport(transaction_data):
    """
    Membuat laporan PDF penjualan tiket bioskop.

    PDF berisi:
    - Ringkasan analisis penjualan
    - Tabel seluruh transaksi
    """

    if not transaction_data:
        print("Tidak ada data transaksi untuk dibuatkan laporan.")
        return

    sales_analysis = analyze(transaction_data)

    # Direktori file Python saat ini
    base_directory = os.path.dirname(__file__)

    # Folder target penyimpanan laporan
    report_directory = os.path.abspath(
        os.path.join(base_directory, "..", "history", "reports")
    )

    # Membuat folder jika belum ada
    os.makedirs(report_directory, exist_ok=True)

    # Timestamp untuk nama file unik
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"REPORT_{timestamp}.pdf"

    # Path lengkap file PDF
    report_file_path = os.path.join(report_directory, report_filename)

    # Membuat dokumen PDF
    pdf_document = SimpleDocTemplate(
        report_file_path,
        pagesize=A4,
    )

    styles = getSampleStyleSheet()
    pdf_elements = []

    # ==========================================================
    # HEADER LAPORAN
    # ==========================================================
    pdf_elements.append(
        Paragraph(
            "LAPORAN PENJUALAN TIKET BIOSKOP CACB",
            styles["Title"],
        )
    )

    pdf_elements.append(Spacer(1, 20))

    printed_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    pdf_elements.append(
        Paragraph(
            f"Tanggal dicetak: {printed_at}",
            styles["Normal"],
        )
    )

    pdf_elements.append(Spacer(1, 25))

    # ==========================================================
    # ANALISIS PENJUALAN
    # ==========================================================
    pdf_elements.append(
        Paragraph(
            "ANALISIS DATA PENJUALAN",
            styles["Heading1"],
        )
    )

    pdf_elements.append(Spacer(1, 10))

    analysis_table_data = [
        ["Total Transaksi", sales_analysis["total_transactions"]],
        ["Total Tiket Terjual", sales_analysis["total_tickets_sold"]],
        [
            "Film Terlaris",
            f"{sales_analysis['best_selling_movie'][0]} "
            f"({sales_analysis['best_selling_movie'][1]} tiket)",
        ],
        [
            "Customer Paling Aktif",
            f"{sales_analysis['most_active_customer'][0]} "
            f"({sales_analysis['most_active_customer'][1]} transaksi)",
        ],
        [
            "Hari Paling Ramai",
            f"{sales_analysis['busiest_day'][0]} "
            f"({sales_analysis['busiest_day'][1]} transaksi)",
        ],
    ]

    analysis_table = Table(
        analysis_table_data,
        colWidths=[180, 350],
    )

    analysis_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    pdf_elements.append(analysis_table)

    # Pindah ke halaman berikutnya
    pdf_elements.append(PageBreak())

    # ==========================================================
    # DATA SELURUH TRANSAKSI
    # ==========================================================
    pdf_elements.append(
        Paragraph(
            "DATA KESELURUHAN TRANSAKSI",
            styles["Heading1"],
        )
    )

    pdf_elements.append(Spacer(1, 15))

    transaction_table_data = [["Kode", "Nama", "Jumlah", "Antrean", "Film", "Tanggal"]]

    for transaction_code, transaction in transaction_data.items():
        transaction_table_data.append(
            [
                transaction_code,
                transaction["nama"],
                transaction["jumlah_tiket"],
                transaction["urutan_antrean"],
                transaction["judul"],
                transaction["date"],
            ]
        )

    transaction_table = Table(
        transaction_table_data,
        colWidths=[55, 55, 45, 50, 150, 150],
        repeatRows=1,
    )

    transaction_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    pdf_elements.append(transaction_table)

    # Generate PDF
    pdf_document.build(pdf_elements)

    print(f"PDF berhasil dibuat: {report_file_path}")
