"""
==========================================================
Seat Sort
Menyortir list kursi dari K1 hingga Kn secara numerik
(bukan alfabet). Contoh: K1, K2, K10 menjadi K1, K2, K10
(bukan K1, K10, K2 yang dihasilkan oleh sort alfabet biasa).

Fungsi/fitur:
1. seat_sort
==========================================================
"""


# ------------------------------
# Nama fungsi: seat_sort
# Penjelasan fungsi : Menyortir list nomor kursi berdasarkan
# bagian numeriknya. Contoh: K12 diurutkan setelah K2
# (bukan sebelum K2 seperti sort alfabet biasa).
# ------------------------------
def seat_sort(seat_list: list):
    """
    Menyortir list kursi secara numerik berdasarkan bagian integer.

    Args:
        seat_list (list): List nomor kursi, contoh: ["K1", "K10", "K2"]

    Returns:
        list: List kursi yang sudah tersortir, contoh: ["K1", "K2", "K10"]
    """
    return sorted(
        seat_list,
        key=lambda x: int("".join(filter(str.isdigit, x)))
    )