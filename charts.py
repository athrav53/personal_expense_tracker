import pandas as pd

def weekly_spending_chart(df):

    if "transaction_date" not in df.columns:
        return None

    temp = df.copy()

    temp["transaction_date"] = pd.to_datetime(
        temp["transaction_date"],
        errors="coerce"
    )

    temp["Day"] = temp["transaction_date"].dt.day_name()

    weekly = (
        temp.groupby("Day")["amount"]
        .sum()
        .reset_index()
    )

    order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekly["Day"] = pd.Categorical(
        weekly["Day"],
        categories=order,
        ordered=True
    )

    weekly = weekly.sort_values("Day")

    return px.bar(
        weekly,
        x="Day",
        y="amount",
        title="Weekly Spending"
    )


def merchant_chart(df):

    if "description" not in df.columns:
        return None

    merchant = (
        df.groupby("description")["amount"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    return px.bar(
        merchant,
        x="description",
        y="amount",
        color="amount",
        title="Top Merchants"
    )


def category_trend(df):

    if "transaction_date" not in df.columns:
        return None

    if "category" not in df.columns:
        return None

    temp = df.copy()

    temp["transaction_date"] = pd.to_datetime(
        temp["transaction_date"],
        errors="coerce"
    )

    temp["Month"] = temp["transaction_date"].dt.strftime("%b")

    trend = (
        temp.groupby(
            ["Month", "category"]
        )["amount"]
        .sum()
        .reset_index()
    )

    return px.line(
        trend,
        x="Month",
        y="amount",
        color="category",
        markers=True,
        title="Category Trend"
    )