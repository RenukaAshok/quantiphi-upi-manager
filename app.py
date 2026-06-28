```python
import streamlit as st
import pandas as pd

st.set_page_config(page_title="UPI Money Manager", layout="wide")

st.title("💳 Bank Transaction UPI Summary & Categorization")
st.markdown("Automated transaction categorization and spending analytics dashboard")

# Sample transaction alerts
transactions = [
    {"message": "Paid Rs. 250 to Zomato", "amount": -250},
    {"message": "Paid Rs. 120 to Uber", "amount": -120},
    {"message": "Received Rs. 45000 from Private Company Ltd", "amount": 45000},
    {"message": "Paid Rs. 500 to Amazon Cashback Offer", "amount": -500},
    {"message": "Paid Rs. 300 to Swiggy", "amount": -300},
    {"message": "Received Rs. 2000 from Friend", "amount": 2000},
]

# Keyword based categorization
def categorize(message):
    msg = message.lower()

    if "zomato" in msg or "swiggy" in msg:
        return "Food & Dining"

    elif "uber" in msg or "ola" in msg:
        return "Travel"

    elif "salary" in msg or "company" in msg or "pvt" in msg:
        return "Salary"

    return "Miscellaneous"


# Cashback detection
def expected_savings(message, amount):
    msg = message.lower()

    reward_keywords = ["cashback", "reward", "amazon"]

    if any(word in msg for word in reward_keywords) and amount < 0:
        return abs(amount) * 0.05

    return 0


# Assign default categories
for txn in transactions:
    txn["category"] = categorize(txn["message"])


# Sidebar category editing
st.sidebar.header("Category Manager")

for txn in transactions:
    txn["category"] = st.sidebar.selectbox(
        txn["message"],
        ["Food & Dining", "Travel", "Salary", "Miscellaneous"],
        index=["Food & Dining", "Travel", "Salary", "Miscellaneous"].index(txn["category"]),
        key=txn["message"]
    )


# Metrics calculation
income = sum(t["amount"] for t in transactions if t["amount"] > 0)
expense = abs(sum(t["amount"] for t in transactions if t["amount"] < 0))
balance = income - expense

category_totals = {
    "Food & Dining": 0,
    "Travel": 0,
    "Salary": 0,
    "Miscellaneous": 0
}

for txn in transactions:
    if txn["amount"] < 0:
        category_totals[txn["category"]] += abs(txn["amount"])

# Top metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Income", f"₹{income:,}")
col2.metric("Total Expense", f"₹{expense:,}")
col3.metric("Net Balance", f"₹{balance:,}")

st.divider()

st.subheader("📊 Spending Distribution")

df_chart = pd.DataFrame(
    {
        "Category": list(category_totals.keys()),
        "Amount": list(category_totals.values())
    }
)

st.bar_chart(df_chart.set_index("Category"))

st.divider()

st.subheader("📈 Category Progress")

max_value = max(category_totals.values()) if max(category_totals.values()) > 0 else 1

for cat, value in category_totals.items():
    st.write(f"**{cat} : ₹{value}**")
    st.progress(value / max_value)

st.divider()

st.subheader("🧾 Transaction Timeline")

for txn in transactions:
    with st.container():
        if txn["amount"] > 0:
            st.success(
                f"{txn['message']} | ₹{txn['amount']:,}"
            )
        else:
            st.error(
                f"{txn['message']} | ₹{abs(txn['amount']):,}"
            )

        st.write(f"Category: **{txn['category']}**")

        savings = expected_savings(txn["message"], txn["amount"])

        if savings > 0:
            st.success(
                f"💚 Expected Savings Reward: ₹{savings:.2f}"
            )

        st.markdown("---")

st.caption("Built using Streamlit for Quantiphi Vibe Coding Round")
```
