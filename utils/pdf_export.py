from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
import os
from datetime import datetime

FONT_PATH = os.path.join(os.path.dirname(__file__), "..", "fonts", "DejaVuSans.ttf")
pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH))


class PageNumCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add the page numbers to the bottom of each page"""
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont('DejaVuSans', 8)
        self.setFillColor(colors.HexColor("#7f8c8d"))
        self.drawString(letter[0] / 2, 30, f"Page {self._pageNumber} of {page_count}")

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
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )
    elements = []
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["h1"],
        fontName="DejaVuSans",
        fontSize=36,
        spaceAfter=24,
        alignment=1,  # Center alignment
        textColor=colors.HexColor("#2c3e50"),  # Dark blue-gray
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["h2"],
        fontName="DejaVuSans",
        fontSize=18,
        spaceAfter=36,
        alignment=1,
        textColor=colors.HexColor("#34495e"),  # Slightly lighter blue-gray
    )
    section_title_style = ParagraphStyle(
        "SectionTitleStyle",
        parent=styles["h2"],
        fontName="DejaVuSans",
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor("#2c3e50"),
        leading=20,
    )
    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontName="DejaVuSans",
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#34495e"),
    )
    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="DejaVuSans",
        fontSize=9,
        textColor=colors.white,
        alignment=1,  # Center alignment for headers
        leading=12,
    )
    footer_style = ParagraphStyle(
        "FooterStyle",
        parent=styles["Normal"],
        fontName="DejaVuSans",
        fontSize=8,
        alignment=1,
        textColor=colors.HexColor("#7f8c8d"),  # Gray
    )

    # Cover Page
    elements.append(Spacer(1, 200))
    elements.append(Paragraph("PayPaladin Summary Report", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    elements.append(Spacer(1, 250))
    elements.append(Paragraph("A comprehensive overview of shared expenses, payments, and settlements.", normal_style))
    elements.append(Spacer(1, 50))
    
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("Confidential", footer_style))

    elements.append(PageBreak())

    # Content Sections
    elements.append(Paragraph("People", section_title_style))
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
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498db")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 16),
                ("TOPPADDING", (0, 0), (-1, 0), 16),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ecf0f1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8f9fa"), colors.HexColor("#e9ecef")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    elements.append(people_table)
    elements.append(PageBreak())
    elements.append(Paragraph("Expenses", section_title_style))
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
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#27ae60")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ecf0f1")),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 14),
                ("TOPPADDING", (0, 0), (-1, 0), 14),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8f9fa"), colors.HexColor("#e9ecef")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),
                ("ALIGN", (5, 0), (5, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(expense_table)
    elements.append(PageBreak())
    elements.append(Paragraph("Payments", section_title_style))
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
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f39c12")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ecf0f1")),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 14),
                ("TOPPADDING", (0, 0), (-1, 0), 14),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8f9fa"), colors.HexColor("#fff3e0")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(payment_table)
    elements.append(PageBreak())
    elements.append(Paragraph("Balances", section_title_style))
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
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498db")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ecf0f1")),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 16),
                ("TOPPADDING", (0, 0), (-1, 0), 16),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8f9fa"), colors.HexColor("#e9ecef")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    elements.append(balance_table)
    elements.append(PageBreak())
    elements.append(Paragraph("Settlements", section_title_style))
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
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e74c3c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ecf0f1")),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 16),
                ("TOPPADDING", (0, 0), (-1, 0), 16),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8f9fa"), colors.HexColor("#fdeded")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    elements.append(settlement_table)

    elements.append(Paragraph("Stats", section_title_style))

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
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7f8c8d")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ecf0f1")),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 16),
                ("TOPPADDING", (0, 0), (-1, 0), 16),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8f9fa"), colors.HexColor("#e9ecef")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    elements.append(net_expense_table)
    elements.append(Spacer(1, 8))

    doc.build(elements, canvasmaker=PageNumCanvas)
