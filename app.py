import streamlit as st
import pandas as pd
from reconciliation import reconcile
from ai_agent import explain_exceptions

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="FinRecon AI",
    page_icon="💼",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("💼 FinRecon AI")
st.subheader("AI-Powered Financial Reconciliation & Exception Analysis")

st.markdown(
    "Automated reconciliation of bank transactions against general-ledger records "
    "with GenAI-powered exception analysis."
)

# -----------------------------
# Load data
# -----------------------------
try:
    bank = pd.read_csv("bank_transactions.csv")
    ledger = pd.read_csv("general_ledger.csv")

except Exception as e:
    st.error(f"Unable to load transaction data: {e}")
    st.stop()

# -----------------------------
# Run reconciliation
# -----------------------------
result = reconcile(bank, ledger)

# -----------------------------
# Calculate KPIs
# -----------------------------
total_transactions = len(result)

matched = (result["status"] == "MATCHED").sum()

exceptions = total_transactions - matched

match_rate = (
    matched / total_transactions * 100
    if total_transactions > 0
    else 0
)

exception_value = result.loc[
    result["status"] != "MATCHED",
    "amount_bank"
].sum()

# -----------------------------
# KPI Dashboard
# -----------------------------
st.markdown("### 📊 Reconciliation Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)

col2.metric(
    "Matched",
    f"{matched:,}"
)

col3.metric(
    "Match Rate",
    f"{match_rate:.1f}%"
)

col4.metric(
    "Exception Value",
    f"₹{exception_value:,.0f}"
)

st.divider()

# -----------------------------
# Charts
# -----------------------------
left, right = st.columns(2)

with left:

    st.markdown("### 🔎 Exception Breakdown")

    exception_counts = (
        result[result["status"] != "MATCHED"]["status"]
        .value_counts()
    )

    st.bar_chart(exception_counts)

with right:

    st.markdown("### 🏢 Exception Value by Vendor")

    vendor_exceptions = (
        result[result["status"] != "MATCHED"]
        .groupby("vendor")["amount_bank"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(vendor_exceptions)

# -----------------------------
# Transaction results
# -----------------------------
st.divider()

st.markdown("### 📋 Reconciliation Results")

status_filter = st.selectbox(
    "Filter by status",
    [
        "All",
        "MATCHED",
        "AMOUNT_MISMATCH",
        "DATE_MISMATCH",
        "MISSING_IN_LEDGER",
        "DUPLICATE"
    ]
)

if status_filter == "All":
    filtered_result = result
else:
    filtered_result = result[
        result["status"] == status_filter
    ]

st.dataframe(
    filtered_result,
    use_container_width=True
)

# -----------------------------
# AI Finance Assistant
# -----------------------------
st.divider()

st.markdown("### 🤖 Finance AI Assistant")

st.write(
    "Generate a natural-language analysis of the verified reconciliation exceptions."
)

if st.button("Generate AI Exception Analysis"):

    summary = {
        "total_transactions": int(total_transactions),
        "matched_transactions": int(matched),
        "match_rate": round(match_rate, 2),
        "exception_count": int(exceptions),
        "exception_value": round(float(exception_value), 2)
    }

    exception_data = (
        result[result["status"] != "MATCHED"]
        [
            [
                "transaction_id",
                "vendor",
                "amount_bank",
                "amount_ledger",
                "status",
                "variance"
            ]
        ]
        .head(30)
    )

    with st.spinner("Analyzing financial exceptions..."):

        analysis = explain_exceptions(
            summary,
            exception_data.to_dict("records")
        )

    st.markdown("#### AI Analysis")

    st.write(analysis)

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "FinRecon AI | Finance Transformation POC | "
    "Python • SQL • GenAI • Streamlit"
)
