# Antrean Tiket Bioskop

A Python-based Command Line Interface (CLI) application for managing cinema ticket bookings by ticketing staff.  
This system implements a Queue to handle customer order processing in a first-come, first-served manner, and a Linked List to efficiently manage booking data

## Team & Role

- **J0403251040** M. Lutfi Ramadhan Warendra (Engineer, Advisor),
- **J0403251070** Fateeh Falah Hendarto (Engineer, Advisor, QA)
- **J0403251098** Wildhan Dzikrihantara (Project Manager, Engineer, QA)

## Dependencies

- `pandas` - for visualizing data tables in `pilihFilm` and `showQueue` (`CRUD/operations/queue.py`)
- `reportlab` - for generating invoice PDFs (`CRUD/operations/invoice.py`)

## How to run

1. Clone this repository or download the ZIP file:

```bash
git clone https://github.com/wilanta/antrian-tiket-bioskop
```

2. Navigate to the project directory:

```bash
cd antrian-tiket-bioskop
```

3. Create a virtual environment and activate it:

```bash
python -m venv venv
```

- Windows:

```bash
venv\Scripts\activate
```

- macOS/Linux/Bash:

```bash
source venv/bin/activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Create the required data files inside the CRUD/data/ directory:

- `data_film.txt`
- `log_pemesanan.txt`

6. Run the application:

```bash
python main.py
```
