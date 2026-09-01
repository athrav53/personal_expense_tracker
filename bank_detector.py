def detect_bank(df):

    columns = [c.lower() for c in df.columns]

    if "narration" in columns:
        return "SBI"

    if "transaction details" in columns:
        return "HDFC"

    if "remarks" in columns:
        return "ICICI"

    if "particulars" in columns:
        return "Axis"

    if "details" in columns:
        return "Barclays"

    return "Unknown"