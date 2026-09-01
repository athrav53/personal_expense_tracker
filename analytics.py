import pandas as pd


def calculate_kpis(df):
    """
    Calculate dashboard KPI values.
    """

    total_income = 0
    total_expense = 0
    current_balance = 0

    if "transaction_type" in df.columns and "amount" in df.columns:

        total_income = df[
            df["transaction_type"] == "Credit"
        ]["amount"].sum()

        total_expense = df[
            df["transaction_type"] == "Debit"
        ]["amount"].sum()

    if "balance" in df.columns and len(df) > 0:
        current_balance = df["balance"].iloc[-1]

    total_transactions = len(df)

    highest_income = 0
    highest_expense = 0

    if "transaction_type" in df.columns:

        income = df[df["transaction_type"] == "Credit"]

        expense = df[df["transaction_type"] == "Debit"]

        if not income.empty:
            highest_income = income["amount"].max()

        if not expense.empty:
            highest_expense = expense["amount"].max()

    average_transaction = 0

    if "amount" in df.columns:
        average_transaction = df["amount"].mean()

    return {
        "income": total_income,
        "expense": total_expense,
        "balance": current_balance,
        "transactions": total_transactions,
        "highest_income": highest_income,
        "highest_expense": highest_expense,
        "average_transaction": average_transaction
    }


def category_summary(df):

    if "category" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )


def monthly_summary(df):

    if "transaction_date" not in df.columns:
        return pd.DataFrame()

    temp = df.copy()

    temp["transaction_date"] = pd.to_datetime(
        temp["transaction_date"]
    )

    temp["Month"] = temp["transaction_date"].dt.strftime("%Y-%m")

    return (
        temp.groupby(
            ["Month", "transaction_type"]
        )["amount"]
        .sum()
        .reset_index()
    )


def top_expenses(df):

    if "transaction_type" not in df.columns:
        return pd.DataFrame()

    return (
        df[df["transaction_type"] == "Debit"]
        .sort_values("amount", ascending=False)
        .head(10)
    )


def top_income(df):

    if "transaction_type" not in df.columns:
        return pd.DataFrame()

    return (
        df[df["transaction_type"] == "Credit"]
        .sort_values("amount", ascending=False)
        .head(10)
    )