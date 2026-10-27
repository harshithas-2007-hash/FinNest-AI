import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FinWise AI | Startup Planner", page_icon="💡", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#102a43,#087f8c); color: white;}
.hero h1 {margin: 0; font-size: 2.35rem;}
.hero p {margin: .5rem 0 0 0; font-size: 1.05rem;}
.small-note {color: #6b7280; font-size: .88rem;}
</style>
<div class="hero">
<h1>FinWise AI</h1>
<p>Your personal financial wellness coach — understand spending, plan savings, and make smarter money decisions.</p>
</div>
""", unsafe_allow_html=True)

st.caption("Student startup prototype • Illustrative assumptions • INR values • Not investment, lending, or tax advice")
tabs = st.tabs(["Product Demo", "5-Year Financial Plan", "Funding Strategy", "How It Works"])

with tabs[0]:
    st.subheader("Try the financial wellness coach")
    c1, c2, c3 = st.columns(3)
    with c1:
        income = st.number_input("Monthly take-home income (₹)", min_value=0, value=30000, step=1000)
    with c2:
        expenses = st.number_input("Monthly expenses (₹)", min_value=0, value=22000, step=500)
    with c3:
        debt = st.number_input("Monthly debt repayments (₹)", min_value=0, value=2000, step=500)
    goal = st.number_input("Savings goal (₹)", min_value=0, value=50000, step=5000)
    months = st.slider("Months to reach savings goal", min_value=1, max_value=36, value=10)
    discretionary = max(income - expenses - debt, 0)
    savings_rate = (discretionary / income * 100) if income else 0
    target_monthly = goal / months if months else 0
    m1, m2, m3 = st.columns(3)
    m1.metric("Estimated monthly surplus", f"₹{discretionary:,.0f}")
    m2.metric("Potential surplus rate", f"{savings_rate:.1f}%")
    m3.metric("Monthly savings needed", f"₹{target_monthly:,.0f}")
    if income == 0:
        st.warning("Enter an income greater than zero to generate a meaningful plan.")
    elif expenses + debt > income:
        st.error(f"Your listed expenses and debt payments exceed income by ₹{expenses + debt - income:,.0f} per month. Review non-essential spending and seek qualified support before taking on new debt.")
    elif discretionary >= target_monthly:
        st.success("Your target appears achievable using the entered figures, provided your actual spending stays on plan.")
    else:
        st.warning(f"Your current surplus is below the target by ₹{target_monthly-discretionary:,.0f} per month. Consider extending the timeline or adjusting the goal.")
    st.markdown("#### Suggested monthly allocation")
    if income > 0:
        allocation = pd.DataFrame({
            "Category": ["Essential expenses", "Debt repayments", "Potential savings / buffer"],
            "Amount": [min(expenses, income), min(debt, max(income-expenses,0)), discretionary]
        })
        fig = px.pie(allocation, names="Category", values="Amount", hole=.55,
                     title="Illustrative allocation of monthly income")
        st.plotly_chart(fig, use_container_width=True)
    st.info("Prototype demo: figures are entered manually. In a production version, users could consent to connect supported account data or upload a transaction CSV. The app does not move money or approve loans.")

with tabs[1]:
    st.subheader("5-year business forecast")
    st.write("Edit the assumptions below. All figures are in **₹ lakh** and are illustrative, not guaranteed results.")
    years = [1, 2, 3, 4, 5]
    default_revenue = [12, 30, 60, 100, 150]
    default_expenses = [28, 38, 52, 72, 98]
    st.markdown("**Revenue streams:** premium subscriptions, institutional licences, and optional financial-wellness workshops.")
    rev_cols = st.columns(5)
    revs = []
    for i, col in enumerate(rev_cols):
        with col:
            revs.append(st.number_input(f"Year {i+1} revenue (₹L)", min_value=0.0, value=float(default_revenue[i]), step=1.0, key=f"rev{i}"))
    exp_cols = st.columns(5)
    exps = []
    for i, col in enumerate(exp_cols):
        with col:
            exps.append(st.number_input(f"Year {i+1} expenses (₹L)", min_value=0.0, value=float(default_expenses[i]), step=1.0, key=f"exp{i}"))
    df = pd.DataFrame({"Year": [f"Year {y}" for y in years], "Revenue (₹L)": revs,
                       "Expenses (₹L)": exps})
    df["Profit / (Loss) (₹L)"] = df["Revenue (₹L)"] - df["Expenses (₹L)"]
    df["Cumulative profit / (loss) (₹L)"] = df["Profit / (Loss) (₹L)"].cumsum()
    a, b, c = st.columns(3)
    a.metric("Year 5 revenue", f"₹{revs[-1]:,.1f}L")
    b.metric("Year 5 profit", f"₹{revs[-1]-exps[-1]:,.1f}L")
    positive = [i+1 for i, p in enumerate(df["Profit / (Loss) (₹L)"]) if p > 0]
    c.metric("First profitable year", f"Year {positive[0]}" if positive else "Not within 5 years")
    st.dataframe(df.style.format({col: "₹{:,.1f}L" for col in df.columns if col != "Year"}), use_container_width=True, hide_index=True)
    chart = px.bar(df, x="Year", y=["Revenue (₹L)", "Expenses (₹L)"], barmode="group", title="Revenue vs expenses")
    st.plotly_chart(chart, use_container_width=True)
    profit_chart = px.line(df, x="Year", y="Profit / (Loss) (₹L)", markers=True, title="Annual profit / loss")
    profit_chart.add_hline(y=0, line_dash="dash")
    st.plotly_chart(profit_chart, use_container_width=True)
    st.download_button("Download forecast as CSV", df.to_csv(index=False).encode("utf-8"), "finwise_ai_5_year_forecast.csv", "text/csv")

with tabs[2]:
    st.subheader("Capital raising plan")
    st.write("A sensible early-stage approach is to combine founder contribution and equity funding, while limiting debt until recurring revenue is more predictable.")
    total = st.number_input("Initial capital required (₹ lakh)", min_value=1.0, value=40.0, step=1.0)
    equity_pct = st.slider("Equity funding share (%)", min_value=0, max_value=100, value=75)
    debt_pct = 100 - equity_pct
    x, y, z = st.columns(3)
    x.metric("Total capital", f"₹{total:.1f}L")
    y.metric(f"Equity ({equity_pct}%)", f"₹{total*equity_pct/100:.1f}L")
    z.metric(f"Debt ({debt_pct}%)", f"₹{total*debt_pct/100:.1f}L")
    fund_df = pd.DataFrame({"Source": ["Founder / angel / seed equity", "Debt / eligible startup credit"], "Share (%)": [equity_pct, debt_pct],
                            "Amount (₹L)": [total*equity_pct/100, total*debt_pct/100]})
    st.plotly_chart(px.pie(fund_df, names="Source", values="Amount (₹L)", hole=.5, title="Illustrative funding mix"), use_container_width=True)
    st.markdown("""
    **Potential capital sources**
    - Founder contribution and university incubator support for validation.
    - Angel investors or seed funds for product development and customer acquisition.
    - Startup competitions, grants, and incubators where eligibility requirements are met.
    - Debt only when repayment capacity is clear; loan availability and terms are not guaranteed.
    """)
    st.warning("Equity dilutes ownership; debt creates repayment obligations. Actual financing requires due diligence and legal/accounting advice.")

with tabs[3]:
    st.subheader("Product architecture and workflow")
    st.markdown("""
    **1. Data input:** Users manually enter income, spending and goals; later, an optional consent-based transaction import can be added.

    **2. Categorisation:** Rules or a machine-learning classifier group transactions into rent, food, travel, bills, shopping and other categories.

    **3. Insight engine:** The app calculates surplus, savings rate, budget variance and whether a goal fits the entered monthly surplus.

    **4. Recommendation layer:** A rules-based coach explains trade-offs in plain language. AI can summarise patterns, but recommendations should be explainable and checked for errors.

    **5. Monetisation:** Free basic tracking; paid premium planning; institution licences; financial-literacy workshops.

    **6. Privacy and compliance:** Encrypt data, collect only necessary information, obtain explicit consent, provide deletion/export controls, and never store bank credentials. Use regulated partners and obtain legal review before offering account aggregation, lending, payments or investment advice.
    """)
    st.markdown("#### Possible APIs for a future production version")
    st.dataframe(pd.DataFrame([
        {"Purpose": "Account data (consent-based)", "Potential route": "India Account Aggregator ecosystem through an authorised partner", "Important note": "Requires eligible regulated participants and consent flows"},
        {"Purpose": "Payments", "Potential route": "UPI/payment gateway partner APIs", "Important note": "Use an authorised provider; do not handle raw payment credentials"},
        {"Purpose": "AI summaries", "Potential route": "LLM API or a self-hosted model", "Important note": "Minimise or redact personal financial data"},
        {"Purpose": "Authentication", "Potential route": "Managed auth provider", "Important note": "Use secure session handling and multi-factor authentication"}
    ]), use_container_width=True, hide_index=True)

st.divider()
st.caption("FinWise AI is a classroom business-plan prototype. Forecasts are assumptions for discussion, not audited projections or financial advice.")
