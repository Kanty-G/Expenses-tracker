import pandas as pd

REQUIRED_COLS = ["id","date","description","amount"]

def load_expenses(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing requires columns: {missing}")
    # Normalize types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if df["date"].isna().any():
        raise ValueError("Some dates could not be parsed. Check 'date' format (YYYY-MM-DD).")

    #Amount: expenses should be positive; if negatives, flip sign
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    if df["amount"].isna().any():
        raise ValueError("Some amounts are not numeric.")
    df.loc[df["amount"] < 0, "amount"] = -df.loc[df["amount"] < 0, "amount"]

    # Optional columns
    if "merchant" not in df.columns:
        df["merchant"] = df["description"].fillna("")

    if "category" not in df.columns:
        df["category"] = pd.NA

    return df
