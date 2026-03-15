"""
==========================================================
ticketSort
Menyortir list tiket dari K1 hingga Kn.
n: Jumlah data dalam list tiket.

Fungsi/fitur:
1. seat_sort
==========================================================
"""


# ````````````````````````````````````````````
# Nama fungsi: seat_sort
# Penjelasan Fungsi : Untuk menyortir list tiket dari K1 hingga Kn
# Dengan n: Jumlah data dalam list tiket
# ````````````````````````````````````````````
def seat_sort(seat_list: list):
    """
    Sortir list tiket dengan sorted, lalu return list.
    Menggunakan function sorted dengan key berdasarkan int yang dipisah dari K
    Sorted dipakai agar data original tidak dimodifikasi

    Args:
        seat_list (list): List Tiket.

    Returns:
        sorted(seat_list) dengan key berdasarkan int yang dipisahkan dari K
    """
    return sorted(
        seat_list,
        key=lambda x: int("".join(filter(str.isdigit, x)))
    )

    # Arg 1: seat_list = list yang disortir dengan func sorted
    # Arg 2: key = sortir berdasarkan sebuah pola
    #   Cara kerja:
    #   1. lambda x = Fungsi anonim yang langsung return satu expression
    #       Anonim berarti tidak perlu di-call di luar function-nya
    #       Plus-nya codebase menjadi lebih clean
    #       Seperti arrow function pada Javascript
    #   2. filter = Hanya pilih digit/bilangan di dalam suatu iterable (seperti str)
    #       str.isdigit = cek jika karakternya berupa bilangan dan return bool
    #       x = dari lambda
    #       Cth: 'K12' -> 'K', '1', '2 -> '1', '2'
    #   3. join = Menggabungkan list menjadi satu string
    #   4. int = Konversi ke int

    # Kenapa gini?
    # Karena mau sort bilangan, bukan abjad
    # String murni: 'K1', 'K2', 'K10' -> 'K1', 'K10', 'K2'
    # Modifikasi string: 'K1', 'K10', 'K2' -> 'K1', 'K2', 'K10'
