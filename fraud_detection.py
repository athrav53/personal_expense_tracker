import pandas as pd


def detect_large_transactions(df, multiplier=3):
    """
    Detect transactions significantly larger than the average.
    """
    if "amount" not in df.columns:
        return pd.DataFrame()

    avg = df["amount"].mean()

    return df[df["amount"] > avg * multiplier]


def detect_duplicate_transactions(df):
    """
    Find duplicate transactions.
    """
    return df[df.duplicated()]


def detect_negative_balance(df):
    """
    Detect negative balances.
    """
    if "balance" not in df.columns:
        return pd.DataFrame()

    return df[df["balance"] < 0]


def merchant_frequency(df):

    if "description" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("description")
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )


def category_spending(df):

    if "category" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )