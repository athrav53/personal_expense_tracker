import streamlit as st
import pandas as pd

from db import get_connection
from queries import GET_ALL_TRANSACTIONS

from column_mapper import standardize_columns
from data_cleaning import clean_data
from bank_detector import detect_bank
from merchant_categorizer import auto_categorize
from file_loader import load_file

from analytics import calculate_kpis

from charts import (
    category_bar_chart,
    credit_debit_pie,
    expense_donut,
    balance_trend,
    monthly_income_expense,
    top_expenses_chart,
    top_income_chart,
    weekly_spending_chart,
    merchant_chart,
    category_trend
)

from insights import generate_insights

from fraud_detection import (
    detect_large_transactions,
    detect_duplicate_transactions,
    detect_negative_balance,
    detect_high_cash_withdrawals,
    detect_repeated_merchants,
    detect_weekend_transactions,
    detect_suspicious_transactions
)

from export import (
    convert_csv,
    convert_excel,
    summary_report
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Universal Bank Statement Analyzer",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Universal Bank Statement Analyzer")
st.caption("Analyse CSV, Excel, PDF & PostgreSQL Bank Statements")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Select Page",
    [
        "Dashboard",
        "Analytics",
        "Transactions",
        "Reports"
    ]
)

st.sidebar.divider()

source = st.sidebar.radio(
    "Data Source",
    [
        "CSV / Excel / PDF",
        "PostgreSQL"
    ]
)

uploaded_file = None

if source == "CSV / Excel / PDF":

    uploaded_file = st.sidebar.file_uploader(
        "Upload Statement",
        type=[
            "csv",
            "xlsx",
            "xls",
            "pdf"
        ]
    )

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = None

try:

    if source == "PostgreSQL":

        conn = get_connection()

        df = pd.read_sql(
            GET_ALL_TRANSACTIONS,
            conn
        )

        conn.close()

        st.sidebar.success(
            "Connected to PostgreSQL"
        )

    else:

        if uploaded_file is None:

            st.info(
                "Please upload a Bank Statement."
            )

            st.stop()

        df = load_file(uploaded_file)

        bank = detect_bank(df)

        st.sidebar.success(
            f"🏦 {bank}"
        )

        st.sidebar.info(
            f"📄 {uploaded_file.name}"
        )

        df = standardize_columns(df)

        df = clean_data(df)

        df = auto_categorize(df)

except Exception as e:

    st.error(e)

    st.stop()

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)

# --------------------------------------------------
# DATASET INFORMATION
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rows",
        len(df)
    )

with col2:
    st.metric(
        "Columns",
        len(df.columns)
    )

with col3:
    st.metric(
        "Missing Values",
        df.isna().sum().sum()
    )

with col4:
    st.metric(
        "Duplicate Rows",
        df.duplicated().sum()
    )

st.divider()

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

kpi = calculate_kpis(df)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Income",
        f"₹{kpi['income']:,.2f}"
    )

with c2:
    st.metric(
        "Expense",
        f"₹{kpi['expense']:,.2f}"
    )

with c3:
    st.metric(
        "Balance",
        f"₹{kpi['balance']:,.2f}"
    )

with c4:
    st.metric(
        "Transactions",
        kpi["transactions"]
    )

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.subheader("Filters")

col1, col2, col3 = st.columns(3)

search = ""

with col1:

    if "description" in df.columns:

        search = st.text_input(
            "Search Description"
        )

with col2:

    if "category" in df.columns:

        category = st.selectbox(
            "Category",
            ["All"] +
            sorted(
                df["category"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    else:

        category = "All"

with col3:

    if "transaction_type" in df.columns:

        transaction = st.selectbox(
            "Transaction Type",
            ["All"] +
            sorted(
                df["transaction_type"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    else:

        transaction = "All"

filtered_df = df.copy()

if search != "":

    filtered_df = filtered_df[
        filtered_df["description"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

if category != "All":

    filtered_df = filtered_df[
        filtered_df["category"] == category
    ]

if transaction != "All":

    filtered_df = filtered_df[
        filtered_df["transaction_type"] == transaction
    ]

st.divider()

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

st.subheader("🤖 AI Financial Insights")

insights = generate_insights(filtered_df)

for item in insights:

    st.success(item)

st.divider()

# --------------------------------------------------
# FINANCIAL SUMMARY
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Highest Income",
        f"₹{kpi['highest_income']:,.2f}"
    )

with col2:

    st.metric(
        "Highest Expense",
        f"₹{kpi['highest_expense']:,.2f}"
    )

with col3:

    st.metric(
        "Average Transaction",
        f"₹{kpi['average_transaction']:,.2f}"
    )

st.divider()

# --------------------------------------------------
# FRAUD DETECTION
# --------------------------------------------------

st.subheader("🚨 Fraud Detection")

large = detect_large_transactions(filtered_df)

duplicate = detect_duplicate_transactions(filtered_df)

negative = detect_negative_balance(filtered_df)

cash = detect_high_cash_withdrawals(filtered_df)

merchant = detect_repeated_merchants(filtered_df)

weekend = detect_weekend_transactions(filtered_df)

suspicious = detect_suspicious_transactions(filtered_df)

if not large.empty:

    st.warning("Large Transactions")

    st.dataframe(
        large,
        use_container_width=True
    )

if not duplicate.empty:

    st.warning("Duplicate Transactions")

    st.dataframe(
        duplicate,
        use_container_width=True
    )

if not negative.empty:

    st.error("Negative Balance Found")

    st.dataframe(
        negative,
        use_container_width=True
    )

if not cash.empty:

    st.warning("High ATM Withdrawals")

    st.dataframe(
        cash,
        use_container_width=True
    )

if not merchant.empty:

    st.info("Frequently Used Merchants")

    st.dataframe(
        merchant,
        use_container_width=True
    )

if not suspicious.empty:

    st.error("Suspicious Transactions")

    st.dataframe(
        suspicious,
        use_container_width=True
    )

st.divider()
# --------------------------------------------------
# DASHBOARD CHARTS
# --------------------------------------------------

st.header("📊 Financial Dashboard")

col1, col2 = st.columns(2)

with col1:

    fig = category_bar_chart(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col2:

    fig = credit_debit_pie(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

col3, col4 = st.columns(2)

with col3:

    fig = expense_donut(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col4:

    fig = balance_trend(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

col5, col6 = st.columns(2)

with col5:

    fig = monthly_income_expense(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col6:

    fig = top_expenses_chart(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

col7, col8 = st.columns(2)

with col7:

    fig = top_income_chart(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col8:

    fig = weekly_spending_chart(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

col9, col10 = st.columns(2)

with col9:

    fig = merchant_chart(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col10:

    fig = category_trend(filtered_df)

    if fig:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# --------------------------------------------------
# REPORTS
# --------------------------------------------------

st.header("📄 Reports & Downloads")

col1, col2 = st.columns(2)

with col1:

    csv = convert_csv(filtered_df)

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="transactions.csv",
        mime="text/csv"
    )

with col2:

    excel = convert_excel(filtered_df)

    st.download_button(
        label="⬇ Download Excel",
        data=excel,
        file_name="transactions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.divider()

# --------------------------------------------------
# SUMMARY REPORT
# --------------------------------------------------

st.subheader("📊 Summary Report")

report = summary_report(filtered_df)

summary_df = pd.DataFrame(
    report.items(),
    columns=["Metric", "Value"]
)

st.dataframe(
    summary_df,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# TRANSACTION TABLE
# --------------------------------------------------

st.header("📋 Transactions")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=600
)

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <center>

    <h4>💰 Universal Bank Statement Analyzer</h4>

    Developed using

    <b>Python | Streamlit | PostgreSQL | Plotly</b>

    </center>
    """,
    unsafe_allow_html=True
)