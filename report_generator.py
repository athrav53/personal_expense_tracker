from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd


def create_pdf_report(
    filename,
    bank_name,
    kpi,
    insights,
    fraud_count
):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    elements = []

    elements.append(
        Paragraph(
            "<b>Universal Bank Statement Analyzer</b>",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"<b>Detected Bank:</b> {bank_name}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "<b>Financial Summary</b>",
            styles["Heading2"]
        )
    )

    table_data = [

        ["Metric", "Value"],

        ["Total Income", f"₹{kpi['income']:,.2f}"],

        ["Total Expense", f"₹{kpi['expense']:,.2f}"],

        ["Balance", f"₹{kpi['balance']:,.2f}"],

        ["Transactions", kpi["transactions"]],

        ["Highest Income", f"₹{kpi['highest_income']:,.2f}"],

        ["Highest Expense", f"₹{kpi['highest_expense']:,.2f}"],

        ["Average Transaction", f"₹{kpi['average_transaction']:,.2f}"]

    ]

    table = Table(table_data)

    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

                ("TEXTCOLOR", (0,0), (-1,0), colors.white),

                ("GRID", (0,0), (-1,-1), 1, colors.black),

                ("BACKGROUND",(0,1),(-1,-1),colors.beige)

            ]

        )

    )

    elements.append(table)

    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(
            "<b>AI Insights</b>",
            styles["Heading2"]
        )
    )

    # `insights` may be a list of strings or a dict of dataframes
    if isinstance(insights, dict):
        for key, val in insights.items():
            if isinstance(val, pd.DataFrame):
                if val.empty:
                    elements.append(Paragraph(f"• {key}: No items detected", styles["Normal"]))
                else:
                    elements.append(Paragraph(f"• {key}: {len(val)} items detected", styles["Normal"]))
                    # try to list a few examples if `description` column exists
                    if "description" in val.columns:
                        for _, r in val.head(5).iterrows():
                            elements.append(Paragraph(f"    - {r['description']}", styles["Normal"]))
            else:
                elements.append(Paragraph(f"• {key}: {str(val)}", styles["Normal"]))
    else:
        for item in insights:
            elements.append(Paragraph("• " + str(item), styles["Normal"]))

    elements.append(Spacer(1,20))

    elements.append(

        Paragraph(

            f"<b>Fraud Alerts:</b> {fraud_count}",

            styles["Heading2"]

        )

    )

    pdf.build(elements)