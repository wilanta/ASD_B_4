from CRUD.utils.clear import _clear  # Mengimpor fungsi clear dari direktori utils yang sama
from rich.console import Console
import time


# ------------------------------
# Nama fungsi: _processing
# Penjelasan fungsi : Menampilkan animasi spinner loading
# dengan pesan status berganti-ganti selama ~3 detik.
# Digunakan sebagai jeda visual saat proses penyimpanan atau pembaruan data.
# ------------------------------
def _processing(msg="Memproses"):
    """
    Menampilkan animasi spinner loading Rich console.

    Args:
        msg (str): Pesan utama yang ditampilkan di sebelah spinner.
    """
    _clear()
    console = Console()
    messages = [
        "Mohon tunggu sebentar...",
        "Sedang memproses data...",
        "Hampir selesai...",
        "Menyimpan perubahan...",
    ]
    with console.status(
        "[bold cyan]{}[/bold cyan]".format(msg), spinner="dots"
    ) as status:
        for i in range(15):
            time.sleep(0.2)
            status.update(
                "[bold cyan]{}[/bold cyan]  [dim]{}[/dim]".format(
                    msg, messages[i % len(messages)]
                )
            )
    _clear()
