import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="EMI Calculator",
    page_icon="🚗",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("❤️ EMI Calculator")
st.write("Calculate your monthly EMI, total payment, and amortization schedule.")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Loan Calculator")

loan_amount = st.sidebar.number_input(
    "Loan Amount (₹)",
    min_value=1000.0,
    value=600000.0,
    step=1000.0
)

interest_rate = st.sidebar.number_input(
    "Annual Interest Rate (%)",
    min_value=0.1,
    value=10.0,
    step=0.1
)

loan_years = st.sidebar.number_input(
    "Loan Tenure (Years)",
    min_value=2,
    value=5,
    step=1
)

# -----------------------------
# EMI Calculation
# -----------------------------
monthly_rate = interest_rate / (12 * 100)
months = loan_years * 12

emi = (
    loan_amount
    * monthly_rate
    * (1 + monthly_rate) ** months
) / (((1 + monthly_rate) ** months) - 1)

total_payment = emi * months
total_interest = total_payment - loan_amount

# -----------------------------
# Display Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Monthly EMI", f"₹ {emi:,.2f}")
col2.metric("Total Interest", f"₹ {total_interest:,.2f}")
col3.metric("Total Payment", f"₹ {total_payment:,.2f}")

st.divider()


# -----------------------------
# Loan Summary
# -----------------------------
st.subheader("Loan Summary")

summary = pd.DataFrame({
    "Item": [
        "Loan Amount",
        "Interest Rate",
        "Loan Tenure",
        "Monthly EMI",
        "Total Interest",
        "Total Payment"
    ],
    "Value": [
        f"₹ {loan_amount:,.2f}",
        f"{interest_rate:.2f} %",
        f"{loan_years} Years",
        f"₹ {emi:,.2f}",
        f"₹ {total_interest:,.2f}",
        f"₹ {total_payment:,.2f}"
    ]
})

st.table(summary)

# -----------------------------
# Pie Chart
# -----------------------------
st.subheader("Payment Distribution")

fig, ax = plt.subplots(figsize=(5, 5))

ax.pie(
    [loan_amount, total_interest],
    labels=["Principal", "Interest"],
    autopct="%1.1f%%",
    startangle=360
)

ax.axis("equal")

st.pyplot(fig)

# -----------------------------
# Amortization Schedule
# -----------------------------
st.subheader("Amortization Schedule")

balance = loan_amount

schedule = []

for month in range(1, months + 1):

    interest = balance * monthly_rate
    principal = emi - interest
    balance -= principal

    if balance < 0:
        balance = 0

    schedule.append([
        month,
        round(emi, 2),
        round(principal, 2),
        round(interest, 2),
        round(balance, 2)
    ])

df = pd.DataFrame(
    schedule,
    columns=[
        "Month",
        "EMI",
        "Principal",
        "Interest",
        "Balance"
    ]
)

st.dataframe(df, use_container_width=True)

# -----------------------------
# Download CSV
# -----------------------------
csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download EMI Schedule",
    data=csv,
    file_name="emi_schedule.csv",
    mime="text/csv"
)