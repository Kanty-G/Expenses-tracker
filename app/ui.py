import streamlit as st
import pandas as pd
from app.data_io import load_data
from app.metrics import (add_revenue, total_revenue, monthly_revenue,
                         avg_spending, orders_per_customer,
                         top_products)

st.set_page_config(page_title="Sales KPI Tracker", layout="wide")
st.title("Sales KPI Tracker")

df = load_data("data/sales_sample.csv")

#sidebar layouts

# Safer date defaults (date_input prefers date objects)
min_d = df["order_date"].min().date()
max_d = df["order_date"].max().date()

date_sel = st.sidebar.date_input("Date range", (min_d, max_d))


# Handle single-date vs range gracefully
if isinstance(date_sel, tuple) and len(date_sel) == 2:
    start_d, end_d = date_sel
else:
    start_d = end_d = date_sel

# Category multiselect (no empty-list errors)
all_categories = sorted(df["category"].dropna().unique().tolist())
cats = st.sidebar.multiselect("Category", all_categories, default=[])


all_channels = sorted(df["channel"].dropna().unique().tolist())
channels = st.sidebar.multiselect("Channel", all_channels, default=all_channels)

# ---------- Build mask robustly ----------
mask = pd.Series(True, index=df.index)

# Date filter
mask &= df["order_date"].dt.date.between(start_d, end_d)

# Category filter (only if user picked some)
if cats:
    mask &= df["category"].isin(cats)

# Channel filter (if user deselected some, filter to remaining)
# If channels is empty, the result will be empty — which is fine/expected.
mask &= df["channel"].isin(channels)

filtered = df.loc[mask]

#--KPIS--
if filtered.empty:
    st.warning("No data for the selected filters.")
else:
    m1,m2,m3 = st.columns(3)
    m1.metric( "Total Revenue", f"${total_revenue(filtered):,.2f}")
    m2.metric("Average spending per customer", f"${avg_spending(filtered):,.2f}")
    m3.metric("Orders per customer", f"{orders_per_customer(filtered):,.2f}")


st.subheader("Monthly Revenue")
mr = monthly_revenue(filtered)
if not mr.empty:
    st.line_chart(mr.set_index("month"))
else:
    st.info("No monthly revenue to display for the current filters.")

st.subheader("Top Products")
tp = top_products(filtered, 5)
if not tp.empty:
    st.bar_chart(tp.set_index("product"))
else:
    st.info("No top products to display for the current filters.")


st.download_button("Download filtered CSV", filtered.to_csv(index=False), "filtered_sales.csv", "text/csv")
