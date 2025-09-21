import streamlit as st
import pandas as pd
from app.data_io import load_expenses
from app.categorize import apply_rules, load_feedback, merge_feedback, save_feedback
from app.metrics import total_spend, expenses_count, top_category, monthly_spend


st.set_page_config(page_title="Expenses Tracker", layout="wide")
st.title("💸 Expenses Tracker")

#load page
df = load_expenses("data/expenses_sample.csv")

# Categorize (rules + saved feedback)
df = apply_rules(df)
fb = load_feedback()
df = merge_feedback(df, fb)

#------- Sidebar filters --------
min_d, max_d = df["date"].min().date(), df["date"].max().date()
date_sel = st.sidebar.date_input("Date range", (min_d, max_d))



# Handle single-date vs range 
if isinstance(date_sel, tuple) and len(date_sel) == 2:
    start_d, end_d = date_sel
else:
    start_d = end_d = date_sel

cats = st.sidebar.multiselect(
    "Category",
    sorted(df["category_final"].dropna().unique().tolist() + ["Uncategorized"]),
)

merchants = st.sidebar.text_input("Merchant contains (optional)", "")

# ---------- Build mask robustly ----------
mask = pd.Series(True, index=df.index)
mask &= df["date"].dt.date.between(start_d, end_d)

# Category filter (only if user picked some)
if cats:
    # normalize nulls as "Uncategorized"
    cat_series = df["category_final"].fillna("Uncategorized")
    mask &= cat_series.isin(cats)

if merchants.strip():
    key = merchants.strip().lower()
    mask &= df["merchant"].str.lower().str.contains(key)

f = df.loc[mask]

# -------- KPIs --------
c1, c2, c3 = st.columns(3)
c1.metric("Total Spend", f"${total_spend(f):,.2f}")
c2.metric("Transactions", f"{expenses_count(f)}")
tc, amt = top_category(f)
c3.metric("Top Category", f"{tc}", delta=f"${amt:,.2f}")

# -------- Charts --------
st.subheader("Monthly Spend")
mr = monthly_spend(f)
if not mr.empty:
    st.line_chart(mr.set_index("month"))
else:
    st.info("No data in this range.")

# -------- Table + quick category fixes --------
st.subheader("Transactions")
show_cols = ["date","description","merchant","amount","category_final","id"]
st.dataframe(f[show_cols].sort_values("date", ascending=False), use_container_width=True)

st.markdown("#### Fix categories")
to_fix = f[f["category_final"].isna()][["id","description","merchant","amount"]].copy()
to_fix["category"] = ""
if not to_fix.empty:
    edited = st.data_editor(to_fix, num_rows="dynamic", use_container_width=True, key="fixcat")
    if st.button("Save category corrections"):
        rows = edited.dropna(subset=["category"])[["id","category"]]
        save_feedback(rows)
        st.success("Saved. Reload the app to apply.")

# -------- Finance Chatbot --------
#st.subheader("Finance Chatbot (beta)")
#q = st.text_input("Ask a question (e.g., 'How much did I spend on Uber last month?')")
#if q:
#    st.write(answer_query(df, q))

# -------- Export --------
st.download_button(
    "Download filtered CSV",
    f.to_csv(index=False),
    "filtered_expenses.csv",
    "text/csv"
)