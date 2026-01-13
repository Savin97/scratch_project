import pandas as pd
import numpy as np

data = {
    "date": pd.date_range(start="2023-01-01", periods=5),
    "ticker": ["AAPL", "NTFLX", "AMZN", "AAPL", "GOOGL"],
    "price": [180, 182, 330, 328, 140],
    "volume": [10_000, 12_000, 9_000, 11_000, 8_000],

}
df = pd.DataFrame(data)

price = df[df["ticker"] == "AAPL"]


df["price_change"] = df["price"].diff()

df["log_return"] = np.log(df["price"] / df["price"].shift(1))
# print(df["log_return"])
df.sort_values("date")
df.sort_values("ticker")

df = df.set_index("date")
df = df.reset_index()

df = df.groupby("ticker").agg(
    sharpe = ("price", lambda x: x.mean()/x.std()),
    return_std=("price", "std"),
    volume_sum=("price", "sum"),

    )
df.to_csv("output.csv", index=False)
print(df)

