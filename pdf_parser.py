import pdfplumber
import pandas as pd


def extract_pdf_tables(pdf_path):
    """
    Extract tables from a bank statement PDF.
    Returns a DataFrame.
    """

    data = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            table = page.extract_table()

            if table:

                for row in table[1:]:
                    data.append(row)

                columns = table[0]

    if len(data) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=columns)

    return df