import pandas as pd

def forecast(df):

    monthly = (

        df.groupby(
            df["transaction_date"].dt.to_period("M")
        )["amount"]

        .sum()

    )

    return monthly.mean()