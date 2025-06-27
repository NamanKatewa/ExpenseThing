from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from datetime import datetime

FONT_PATH = os.path.join(os.path.dirname(__file__), "..", "fonts", "DejaVuSans.ttf")
pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH))


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
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=24,
        leftMargin=24,
        topMargin=24,
        bottomMargin=24,
    )
    elements = []
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    section_style = styles["Heading2"]
    normal_style = ParagraphStyle(
        "Normal", parent=styles["Normal"], fontName="DejaVuSans", fontSize=10
    )
    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="DejaVuSans",
        fontSize=10,
        textColor=colors.white,
    )

    elements.append(Paragraph("PayPaladin Summary", title_style))
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("People", section_style))
    elements.append(
        Paragraph(
            "List of all participants involved in the shared expenses.", normal_style
        )
    )
    people_data = [[Paragraph("Name", table_header_style)]]
    for p in people:
        people_data.append([Paragraph(str(p), normal_style)])
    people_table = Table(people_data, hAlign="LEFT", colWidths=[200])
    people_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1976d2")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.whitesmoke, colors.lightblue],
                ),
            ]
        )
    )
    elements.append(people_table)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Expenses", section_style))
    elements.append(
        Paragraph(
            "All recorded expenses including description, amount, who paid, who was involved, how much each person owes, and the date of the expense.",
            normal_style,
        )
    )

    elements.append(Spacer(1, 8))
    expense_data = [
        [
            Paragraph(h, table_header_style)
            for h in [
                "ID",
                "Description",
                "Amount",
                "Paid By",
                "Involved",
                "Each Owes",
                "Date",
            ]
        ]
    ]
    for e in expenses:
        expense_data.append(
            [
                Paragraph(str(getattr(e, "id", "")), normal_style),
                Paragraph(str(getattr(e, "description", "")), normal_style),
                Paragraph(f"₹{getattr(e, 'amount', 0):,.2f}", normal_style),
                Paragraph(str(getattr(e, "paid_by", "")), normal_style),
                Paragraph(", ".join(getattr(e, "involved_people", [])), normal_style),
                Paragraph(
                    f"₹{getattr(e, 'split_amount_per_person', 0):,.2f}", normal_style
                ),
                Paragraph(format_date(getattr(e, "date", "")), normal_style),
            ]
        )

    expense_col_widths = [28, 80, 60, 55, 180, 60, 84]

    expense_table = Table(expense_data, hAlign="LEFT", colWidths=expense_col_widths)
    expense_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#388e3c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.whitesmoke, colors.HexColor("#e8f5e9")],
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),
                ("ALIGN", (5, 0), (5, -1), "RIGHT"),
            ]
        )
    )
    elements.append(expense_table)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Payments", section_style))
    elements.append(
        Paragraph(
            "Payments made directly between participants to settle expenses (outside of automatic calculations).",
            normal_style,
        )
    )

    payment_data = [
        [
            Paragraph(h, table_header_style)
            for h in ["ID", "Description", "Amount", "From", "To", "Date"]
        ]
    ]
    for p in payments:
        payment_data.append(
            [
                Paragraph(str(getattr(p, "id", "")), normal_style),
                Paragraph(str(getattr(p, "description", "")), normal_style),
                Paragraph(f"₹{getattr(p, 'amount', 0):,.2f}", normal_style),
                Paragraph(str(getattr(p, "payer", "")), normal_style),
                Paragraph(str(getattr(p, "payee", "")), normal_style),
                Paragraph(format_date(getattr(p, "date", "")), normal_style),
            ]
        )
    payment_table = Table(
        payment_data, hAlign="LEFT", colWidths=[30, 90, 70, 60, 60, 120]
    )
    payment_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fbc02d")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.whitesmoke, colors.HexColor("#fffde7")],
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    elements.append(payment_table)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Balances", section_style))
    elements.append(
        Paragraph(
            "Final balance for each person after considering all expenses and payments. Positive means they are owed, negative means they owe others.",
            normal_style,
        )
    )

    balance_data = [
        [
            Paragraph("Person", table_header_style),
            Paragraph("Balance (₹)", table_header_style),
        ]
    ]
    for person, amount in balances.items():
        balance_data.append(
            [
                Paragraph(person, normal_style),
                Paragraph(f"₹{amount:,.2f}", normal_style),
            ]
        )
    balance_table = Table(balance_data, hAlign="LEFT", colWidths=[120, 100])
    balance_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0288d1")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.whitesmoke, colors.HexColor("#e1f5fe")],
                ),
            ]
        )
    )
    elements.append(balance_table)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Settlements", section_style))
    elements.append(
        Paragraph(
            "Suggested payments to settle all balances so that everyone ends up even. These are the minimum number of transactions required.",
            normal_style,
        )
    )

    settlement_data = [
        [Paragraph(h, table_header_style) for h in ["From", "To", "Amount (₹)"]]
    ]
    if settlements:
        for s in settlements:
            settlement_data.append(
                [
                    Paragraph(s["from"], normal_style),
                    Paragraph(s["to"], normal_style),
                    Paragraph(f"₹{s['amount']:,.2f}", normal_style),
                ]
            )
    else:
        settlement_data.append(
            [Paragraph("No settlements needed.", normal_style), "", ""]
        )
    settlement_table = Table(settlement_data, hAlign="LEFT", colWidths=[100, 100, 100])
    settlement_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d32f2f")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.whitesmoke, colors.HexColor("#ffebee")],
                ),
            ]
        )
    )
    elements.append(settlement_table)

    stats_style = ParagraphStyle(
        "StatsHeader",
        parent=styles["Heading2"],
        fontName="DejaVuSans",
        textColor=colors.HexColor("#6d4c41"),
    )
    elements.append(Paragraph("Stats", stats_style))

    elements.append(Spacer(1, 8))

    total_expenses = sum(getattr(e, "amount", 0) for e in expenses)
    elements.append(
        Paragraph(f"<b>Total Expenses:</b> ₹{total_expenses:,.2f}", normal_style)
    )

    elements.append(Spacer(1, 8))

    elements.append(
        Paragraph(
            "The total share of expenses each person was responsible for, based on how many expenses they were part of.",
            normal_style,
        )
    )

    net_expense_by_person = {p: 0 for p in people}
    for e in expenses:
        split = getattr(e, "split_amount_per_person", 0)
        for person in getattr(e, "involved_people", []):
            net_expense_by_person[person] = net_expense_by_person.get(person, 0) + split

    net_expense_data = [
        [
            Paragraph("Person", table_header_style),
            Paragraph("Net Expense (₹)", table_header_style),
        ]
    ]
    for person, amount in sorted(
        net_expense_by_person.items(), key=lambda x: x[1], reverse=True
    ):
        net_expense_data.append(
            [
                Paragraph(person, normal_style),
                Paragraph(f"₹{net_expense_by_person[person]:,.2f}", normal_style),
            ]
        )
    net_expense_table = Table(net_expense_data, hAlign="LEFT", colWidths=[120, 120])
    net_expense_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#8d6e63")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.whitesmoke, colors.HexColor("#d7ccc8")],
                ),
            ]
        )
    )
    elements.append(net_expense_table)
    elements.append(Spacer(1, 8))

    doc.build(elements)
