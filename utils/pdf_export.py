from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
import pdfkit

# Configure path to wkhtmltopdf executable
# IMPORTANT: You need to install wkhtmltopdf separately.
# Download from https://wkhtmltopdf.org/downloads.html
# And update this path to where wkhtmltopdf.exe is located on your system.
# For Windows, a common default path is 'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
# You can also set this as an environment variable named WKHTMLTOPDF_PATH.
WKHTMLTOPDF_PATH = os.environ.get('WKHTMLTOPDF_PATH', r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# Ensure the path exists before configuring pdfkit
if not os.path.exists(WKHTMLTOPDF_PATH):
    print(f"Warning: wkhtmltopdf executable not found at {WKHTMLTOPDF_PATH}. Please install it or set the WKHTMLTOPDF_PATH environment variable.")
    # Fallback to trying to find it in PATH, though this might not work if not explicitly set
    config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf')
else:
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

def format_date(dt):
    if isinstance(dt, str):
        try:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S.%f"):
                try:
                    dt = datetime.strptime(dt, fmt)
                    break
                except ValueError:
                    continue
        except Exception:
            return str(dt)
    if isinstance(dt, datetime):
        return dt.strftime("%b %d, %Y, %I:%M %p")
    return str(dt)


def export_summary_to_pdf(filename, people, expenses, payments, balances, settlements):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Setup Jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("pdf_report_template.html")

    # Prepare data for the template
    total_expenses = sum(getattr(e, "amount", 0) for e in expenses)
    net_expense_by_person = {p: 0 for p in people}
    for e in expenses:
        split = getattr(e, "split_amount_per_person", 0)
        for person in getattr(e, "involved_people", []):
            net_expense_by_person[person] = net_expense_by_person.get(person, 0) + split

    # Sort net expenses for consistent output
    sorted_net_expense_by_person = dict(sorted(net_expense_by_person.items(), key=lambda x: x[1], reverse=True))

    context = {
        "generated_date": datetime.now().strftime("%B %d, %Y"),
        "people": people,
        "expenses": expenses,
        "payments": payments,
        "balances": balances,
        "settlements": settlements,
        "total_expenses": total_expenses,
        "net_expense_by_person": sorted_net_expense_by_person,
        "format_date": format_date, # Pass the function to the template
    }

    # Render HTML
    html_out = template.render(context)

    # Generate PDF using pdfkit
    # Options for pdfkit can be added here if needed, e.g., for header/footer
    options = {
        'enable-local-file-access': None, # Required for local file access (e.g., fonts)
        'encoding': "UTF-8",
    }
    try:
        pdfkit.from_string(html_out, filename, configuration=config, options=options)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        print("Please ensure wkhtmltopdf is installed and its path is correctly configured.")
