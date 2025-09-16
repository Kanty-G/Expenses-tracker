import pandas as pd
import numpy as np
import random

# Sample data
n = 50
dates = pd.date_range("2024-01-01", periods=180).to_list()
products = ["Laptop", "Headphones", "Keyboard", "Mouse", "Monitor"]
categories = ["Electronics", "Accessories"]
cities = ["Montreal", "Toronto", "Vancouver"]
channels = ["Online", "In-Store"]

df = pd.DataFrame({
    "order_id": [f"ORD{i:04d}" for i in range(1, n+1)],
    "order_date": np.random.choice(dates, n),
    "customer_id": np.random.randint(1000, 2000, n),
    "product": np.random.choice(products, n),
    "category": np.random.choice(categories, n),
    "qty": np.random.randint(1, 5, n),
    "unit_price": np.random.randint(20, 500, n),
    "city": np.random.choice(cities, n),
    "channel": np.random.choice(channels, n)
})

df.to_csv("sales_sample.csv", index=False)
print("✅ CSV generated: sales_sample.csv")
