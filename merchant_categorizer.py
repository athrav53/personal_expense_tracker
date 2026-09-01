import pandas as pd


MERCHANT_RULES = {

    "Food": [
        "zomato",
        "swiggy",
        "dominos",
        "pizza hut",
        "kfc",
        "mcdonald",
        "starbucks",
        "restaurant",
        "cafe"
    ],

    "Shopping": [
        "amazon",
        "flipkart",
        "myntra",
        "ajio",
        "meesho",
        "nykaa"
    ],

    "Transport": [
        "uber",
        "ola",
        "rapido",
        "metro",
        "petrol",
        "fuel",
        "hpcl",
        "bpcl",
        "indian oil"
    ],

    "Bills": [
        "electricity",
        "water",
        "gas",
        "bsnl",
        "airtel",
        "jio",
        "vi",
        "vodafone"
    ],

    "Entertainment": [
        "netflix",
        "spotify",
        "prime",
        "hotstar",
        "youtube",
        "sony liv"
    ],

    "Healthcare": [
        "apollo",
        "hospital",
        "medical",
        "pharmacy",
        "chemist",
        "clinic"
    ],

    "Salary": [
        "salary",
        "payroll",
        "wages",
        "income"
    ],

    "ATM": [
        "atm",
        "cash withdrawal"
    ],

    "Transfer": [
        "upi",
        "imps",
        "neft",
        "rtgs"
    ]
}


def auto_categorize(df):

    if "description" not in df.columns:
        return df

    if "category" not in df.columns:
        df["category"] = ""

    for index, row in df.iterrows():

        description = str(row["description"]).lower()

        for category, keywords in MERCHANT_RULES.items():

            if any(keyword in description for keyword in keywords):

                df.at[index, "category"] = category
                break

    df["category"] = df["category"].replace("", "Others")

    return df