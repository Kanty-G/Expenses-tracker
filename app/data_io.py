import pandas as pd

REQUIRED_COLS = ["order_id","order_date","customer_id","product","category","qty","unit_price","city","channel"]

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    if df["order_date"].isna().any():
        raise ValueError("Unparseable dates in order_date.")
    if (df["qty"] < 0).any() or (df["unit_price"] < 0).any():
        raise ValueError("Negative values in qty/unit_price.")
    return df
