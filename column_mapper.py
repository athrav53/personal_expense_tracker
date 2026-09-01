COLUMN_MAPPING = {
    "Date": "transaction_date",
    "Txn Date": "transaction_date",
    "Transaction Date": "transaction_date",

    "Description": "description",
    "Narration": "description",
    "Remarks": "description",

    "Debit": "debit",
    "Withdrawal": "debit",
    "Debit Amount": "debit",

    "Credit": "credit",
    "Deposit": "credit",
    "Credit Amount": "credit",

    "Balance": "balance",
    "Closing Balance": "balance",

    "Category": "category"
}


def standardize_columns(df):
    """Rename dataframe columns using the COLUMN_MAPPING dict.

    Unknown columns are lowercased and spaces replaced with underscores.
    """
    cols = {}

    for c in df.columns:
        # try exact match first
        if c in COLUMN_MAPPING:
            cols[c] = COLUMN_MAPPING[c]
            continue

        # try case-insensitive match
        for k, v in COLUMN_MAPPING.items():
            if c.strip().lower() == k.strip().lower():
                cols[c] = v
                break

        # fallback: normalized form
        if c not in cols:
            cols[c] = c.strip().lower().replace(" ", "_")

    return df.rename(columns=cols)