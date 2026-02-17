"""
==========================================================
Node Generator
Membuat node untuk digunakan pada linked list dan queue

Fungsi/fitur:
1. generateNode
==========================================================
"""

# ------------------------------
# Nama fungsi: create node
# Penjelasan fungsi : Untuk membuat node yang akan digunakan pada linked list dan queue.
# ------------------------------
def generateNode(data):
    return {"data": data, "next": None}