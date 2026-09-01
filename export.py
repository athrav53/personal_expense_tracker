import pandas as pd
from io import BytesIO


def convert_csv(df):
    """
    Convert DataFrame to CSV
    """
    return df.to_csv(index=False).encode("utf-8")


def convert_excel(df):
    """
    Convert DataFrame to Excel
    """

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Transactions"
        )

    return output.getvalue()


def summary_report(df):

    report = {}

    report["Total Transactions"] = len(df)

    if "amount" in df.columns:

        report["Total Amount"] = round(
            df["amount"].sum(),
            2
        )

        report["Average Amount"] = round(
            df["amount"].mean(),
            2
        )

        report["Highest Transaction"] = round(
            df["amount"].max(),
            2
        )

        report["Lowest Transaction"] = round(
            df["amount"].min(),
            2
        )

    if "transaction_type" in df.columns:

        report["Total Credit"] = round(

            df[
                df["transaction_type"] == "Credit"
            ]["amount"].sum(),

            2

        )

        report["Total Debit"] = round(

            df[
                df["transaction_type"] == "Debit"
            ]["amount"].sum(),

            2

        )

    if "category" in df.columns:

        report["Top Category"] = (

            df.groupby("category")["amount"]

            .sum()

            .idxmax()

        )

    return report