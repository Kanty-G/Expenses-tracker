import os
import re
import pandas as pd

#map categories to regex patterns

KEYWORDS_MAP = {
    "Transport": [r"\buber\b", r"\blyft\b", r"\btaxi\b", r"\bstm\b", r"\bmetro\b", r"\bbus\b", r"\btrain\b", r"\bflight\b"],
    "Groceries": [r"\bsupermarket\b", r"\bgrocery\b", r"\bmarket\b", r"\bwhole foods\b", r"\bawalmart\b", r"\bcostco\b", r"\biga\b",
                   r"\bmetro\b", r"\bmaxi\b", r"\bprovigo\b", r"\bsobeys\b", r"\bfood basics\b"], 
    "Dining": [r"\brestaurant\b", r"\bcafe\b", r"\bcoffee\b", r"\bbar\b", r"\bpizza\b", r"\bburger\b", r"\bsushi\b",
                r"\bchipotle\b", r"\bsubway\b", r"\btim\s*h(a|o)rton", r"\bmcdo(nald'?s)?\b", r"\bkfc\b", r"\bdomino'?s\b"],
    "Entertainment": [r"\bmovie\b", r"\btheater\b", r"\bconcert\b", r"\bmuseum\b", r"\bfestival\b"],
    "Subscriptions": [r"\bnetflix\b", r"\bspotify\b", r"\bhulu\b", r"\bdisney\+?\b", r"\bprime\b", r"\byoutube\s*premium\b", r"\bapple\s*music\b"],
    "Utilities": [r"\bhydro\b", r"\bbell\b", r"\bgas\b", r"\binternet\b", r"\bvideotron\b", r"\brogers\b", r"\btelus\b", r"\bsasktel\b"],
    "Shopping": [r"\bamazon\b", r"\beBay\b", r"\betsy\b", r"\bmall\b", r"\bclothing\b", r"\bshoes\b", r"\bfashion\b", r"\bh&m\b"].
}

FEEDBACK_PATH = "data/category_feedback.csv"

def rule_category(text:str) -> str | None:
    if not isinstance(text, str):
        return None
    t = text.lower()
    for cat, patterns in KEYWORDS_MAP.items():
        if any ( re. search(p, t) for p in patterns):
            return cat
    return None

def apply_rules(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["category_rule"] = out["category"]
    need = out["category_rule"].isna()
    out.loc[need, "category_rule"] = out.loc[need, "description"].map(rule_category)
    return out

def load_feedback(path: str = FEEDBACK_PATH) -> pd.DataFrame:
    if not os.path.exists(FEEDBACK_PATH):
        return pd.read_csv(FEEDBACK_PATH)
    return pd.DataFrame(columns=["id", "category"])
def merge_feedback(df: pd.DataFrame, fb: pd.DataFrame) -> pd.DataFrame:
    if fb.empty:
        df["category_final"] = df["category_rule"]
        return df
    out = df.merge(fb, on="id", how="left", suffixes=("","_fb"))
    out["category_final"] = out["category_fb"].combine_first(out["category_rule"])
    return out

def save_feedback(rows: pd.DataFrame) -> None:
    # rows must have ["id","category"]
    if rows.empty:
        return
    exists = os.path.exists(FEEDBACK_PATH)
    rows[["id","category"]].to_csv(FEEDBACK_PATH, mode="a", header=not exists, index=False)

        