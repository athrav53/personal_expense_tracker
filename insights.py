import pandas as pd


def detect_large_transactions(df: pd.DataFrame, threshold: float | None = None) -> pd.DataFrame:
    """Return transactions whose absolute amount exceeds a threshold.

    If `threshold` is None, compute `mean(abs(amount)) + 3*std(abs(amount))`.
    """
    if "amount" not in df.columns:
        return pd.DataFrame()

    amounts = df["amount"].abs()

    if threshold is None:
        mean = amounts.mean()
        std = amounts.std()
        threshold = mean + 3 * std if pd.notna(std) else mean * 2

    return df[amounts > threshold].copy()


def detect_duplicate_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows that appear to be duplicates based on date, amount and description."""
    cols = [c for c in ("transaction_date", "amount", "description") if c in df.columns]
    if not cols:
        return pd.DataFrame()

    dup_mask = df.duplicated(subset=cols, keep=False)
    return df[dup_mask].copy()


def detect_negative_balance(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows where the `balance` column is negative."""
    if "balance" not in df.columns:
        return pd.DataFrame()

    return df[df["balance"] < 0].copy()


def generate_insights(df: pd.DataFrame) -> dict:
    """Generate a small set of fraud/risk insights using the detectors.

    Returns a dict with keys: `large`, `duplicate`, `negative`, where each
    value is a DataFrame (may be empty).
    """
    return {
        "large": detect_large_transactions(df),
        "duplicate": detect_duplicate_transactions(df),
        "negative": detect_negative_balance(df),
    }
