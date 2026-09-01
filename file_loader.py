import pandas as pd
import tempfile
from pdf_parser import extract_pdf_tables


def load_file(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):

        return pd.read_csv(uploaded_file)

    elif filename.endswith(".xlsx"):

        return pd.read_excel(uploaded_file)

    elif filename.endswith(".xls"):

        return pd.read_excel(uploaded_file)

    elif filename.endswith(".pdf"):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

            tmp.write(uploaded_file.read())

            return extract_pdf_tables(tmp.name)

    else:

        raise ValueError("Unsupported file format")