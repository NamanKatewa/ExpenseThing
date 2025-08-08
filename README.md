## ExpenseThing

Minimal CLI to track, split, and settle shared expenses. Data persists to JSON in `data/`. Optional PDF report.

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

