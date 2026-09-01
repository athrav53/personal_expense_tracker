import pandas as pd


def insert_transactions(conn, df):

    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute(
            """
            INSERT INTO bank_transactions
            (
                transaction_date,
                description,
                transaction_type,
                category,
                amount,
                balance
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                row.get("transaction_date"),
                row.get("description"),
                row.get("transaction_type"),
                row.get("category"),
                row.get("amount"),
                row.get("balance"),
            )
        )

    conn.commit()
    cursor.close()


def delete_all_transactions(conn):

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM bank_transactions;
        """
    )

    conn.commit()
    cursor.close()


def transaction_count(conn):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM bank_transactions;
        """
    )

    count = cursor.fetchone()[0]

    cursor.close()

    return count
