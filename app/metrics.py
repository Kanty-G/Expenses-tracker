import pandas as pd


# Function to add a revenue column to the DataFrame
def add_revenue(df: pd.DataFrame) -> pd.DataFrame:

    out = df.copy()
    out["revenue"] = out["qty"] * out["unit_price"]
    return out

# Function to calculate total revenue
def total_revenue(df: pd.DataFrame) -> float:
    return float((df["qty"] * df["unit_price"]).sum())

# Function to calculate monthly revenue
def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    k = df.assign(month = df["order_date"].dt.to_period("M").dt.to_timestamp())
    return k.groupby("month", as_index=False).apply(lambda x: (x["qty"] * x["unit_price"]).sum()).rename(columns={0: "monthly_revenue"})

#Function to calculate average spending per customer
def avg_spending(df: pd.DataFrame) -> float:
    orders = len(df)
    return float((df["qty"] * df["unit_price"]).sum() / orders) if orders  else 0.0

# Function to calculate ordders per customer
def orders_per_customer(df: pd.DataFrame) -> float:
    customers = df["customer_id"].nunique()
    return float(len(df) / customers) if customers else 0.0

#Function to get the top bought products
def top_products(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    k = df.assign(revenue = df["qty"] * df["unit_price"]).groupby("product", as_index=False)["revenue"].sum()
    return k.sort_values(["revenue", "product"], ascending=[False, True]).head(n)
