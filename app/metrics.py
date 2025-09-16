import pandas as pd


# Function to get total spent on a certain period
def total_spend(df: pd.DataFrame) -> float:
    return float(df["amount"].sum())

def expenses_count(df: pd.DataFrame) -> int:
    return int(len(df))
    
# Function to get the top category by spending
def top_category(df: pd.DataFrame) -> tuple[str, float] | tuple[str, float]:
    if  df.empty or "category_final" not in df.columns:
        return ("N/A", 0.0)  
    k = df.groupby("category_final", dropna = False)["amount"].sum().sort_values(ascending=False)
    if k.empty:
        return ("N/A", 0.0)
    return (k.index[0] if pd.notna(k.index[0]) else "Uncategorized", float(k.iloc[0]))

def monthy_spend(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["month", "amount"])
    k = dg.assign(month = df["date"].dt.to_period("M").dt.to_timestamp())
    return k.groupby("month", as_index=False)["amount"].sum()
    
