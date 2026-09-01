import pandas as pd


def generate_insights(df):
    """
    Generate summary insights from bank statement data.
    """

    insights = []

    # Highest Expense
    if "transaction_type" in df.columns:
        expense = df[df["transaction_type"] == "Debit"]

        if not expense.empty:
            highest = expense.loc[expense["amount"].idxmax()]

            insights.append(
                f"Highest expense was ₹{highest['amount']:,.2f} on '{highest['description']}'."
            )

    # Highest Income
    if "transaction_type" in df.columns:
        income = df[df["transaction_type"] == "Credit"]

        if not income.empty:
            highest = income.loc[income["amount"].idxmax()]

            insights.append(
                f"Highest income was ₹{highest['amount']:,.2f} from '{highest['description']}'."
            )

    # Most Expensive Category
    if "category" in df.columns:
        category = (
            df[df["transaction_type"] == "Debit"]
            .groupby("category")["amount"]
            .sum()
        )

        if not category.empty:
            top = category.idxmax()

            insights.append(
                f"Highest spending category: {top} (₹{category.max():,.2f})"
            )

    # Average Expense
    expense = df[df["transaction_type"] == "Debit"]

    if not expense.empty:

        insights.append(
            f"Average expense per transaction: ₹{expense['amount'].mean():,.2f}"
        )

    # Average Income
    income = df[df["transaction_type"] == "Credit"]

    if not income.empty:

        insights.append(
            f"Average income per transaction: ₹{income['amount'].mean():,.2f}"
        )

    # Total Transactions
    insights.append(
        f"Total transactions analysed: {len(df)}"
    )

    return insights