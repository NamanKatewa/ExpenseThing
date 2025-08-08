## ExpenseThing

ExpenseThing is a command-line interface (CLI) application built with Python for tracking, splitting, and settling shared expenses. It allows users to manage group expenses, record payments, and view balances efficiently. The application persists data in JSON format and offers an optional feature to export expense reports as PDF files.

### Tools and Technologies

* **Python:** The core programming language used for the application.
* **Click:** A Python package for creating beautiful command-line interfaces.
* **pdfkit:** A Python library to convert HTML to PDF, used for generating expense reports.
* **Jinja2:** A modern and designer-friendly templating engine for Python, used for creating the PDF report template.

### Install

- Python 3.9+
- From project root:

```bash
python -m venv venv
./venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
```

### PDF export (optional)

Install `wkhtmltopdf` and add it to PATH or set `WKHTMLTOPDF_PATH` (e.g., `C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe`).

### Commands

Run from project root:

```bash
python cli.py --help
python cli.py add
python cli.py pay
python cli.py view
python cli.py view-payments
python cli.py add-person
python cli.py list-people
python cli.py balances
python cli.py settle
python cli.py export-pdf --filename report.pdf
```

### Notes

- Creates `data/expenses.json`, `data/payments.json`, `data/people.json` automatically.
- PDFs save under `data/` (default filename includes a timestamp).

