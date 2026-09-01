import pandas as pd


def clean_data(df):
    """
    Clean and standardize bank statement data.
    """

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove empty rows
    df = df.dropna(how="all")

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Clean debit column
    if "debit" in df.columns:
        df["debit"] = (
            df["debit"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
        )
        df["debit"] = pd.to_numeric(df["debit"], errors="coerce").fillna(0)

    # Clean credit column
    if "credit" in df.columns:
        df["credit"] = (
            df["credit"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
        )
        df["credit"] = pd.to_numeric(df["credit"], errors="coerce").fillna(0)

    # Clean balance column
    if "balance" in df.columns:
        df["balance"] = (
            df["balance"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
        )
        df["balance"] = pd.to_numeric(df["balance"], errors="coerce")

    # Convert transaction date
    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(
            df["transaction_date"],
            errors="coerce"
        )

    # Create amount column
    if "debit" in df.columns and "credit" in df.columns:

        df["amount"] = df["credit"]

        debit_rows = df["debit"] > 0

        df.loc[debit_rows, "amount"] = df.loc[debit_rows, "debit"]

    # Create transaction type
    if "debit" in df.columns and "credit" in df.columns:

        df["transaction_type"] = "Credit"

        df.loc[df["debit"] > 0, "transaction_type"] = "Debit"

    return df