GET_ALL_TRANSACTIONS = """
SELECT *
FROM bank_transactions
ORDER BY transaction_date DESC;
"""

TOTAL_CREDIT = """
SELECT COALESCE(SUM(amount),0)
FROM bank_transactions
WHERE transaction_type='Credit';
"""

TOTAL_DEBIT = """
SELECT COALESCE(SUM(amount),0)
FROM bank_transactions
WHERE transaction_type='Debit';
"""

CATEGORY_SUMMARY = """
SELECT
    category,
    SUM(amount) AS total_amount
FROM bank_transactions
GROUP BY category
ORDER BY total_amount DESC;
"""

MONTHLY_SUMMARY = """
SELECT
    DATE_TRUNC('month', transaction_date) AS month,
    transaction_type,
    SUM(amount) AS total_amount
FROM bank_transactions
GROUP BY month, transaction_type
ORDER BY month;
"""

TOP_10_EXPENSES = """
SELECT *
FROM bank_transactions
WHERE transaction_type='Debit'
ORDER BY amount DESC
LIMIT 10;
"""