import pandas as pd
import numpy as np

data = {
    "date": pd.date_range(start="2023-01-01", periods=5),
    "ticker": ["AAPL", "NTFLX", "AMZN", "AAPL", "GOOGL"],
    "price": [180, 182, 330, 328, 140],
    "volume": [10_000, 12_000, 9_000, 11_000, 8_000],

}
df = pd.DataFrame(data)


df["price_change"] = df["price"].diff()

df["log_return"] = np.log(df["price"] / df["price"].shift(1))
# print(df["log_return"])
# print(df.head())

df = df.sort_values(["ticker", "date"])


df = df.set_index("date")
df = df.reset_index()

df["mean_price"] = (
    df.groupby("ticker")["price"].transform("mean")
)

df = df.groupby(["ticker"]).filter(lambda x: len(x)>1)

df["ret"] = df.groupby("ticker")["price"].pct_change()

df["vol_20"] = (
    df.groupby("ticker")["ret"].rolling(20).std().reset_index(level=0,drop=True)
)

# print(df.head())


##
df = pd.DataFrame({
    "ticker": ["AAPL", "AAPL", "AAPL", "MSFT", "MSFT"],
    "date": pd.to_datetime([
        "2024-01-01",
        "2024-01-02",
        "2024-01-03",
        "2024-01-01",
        "2024-01-02",
    ]),
    "price": [100, 102, 104, 200, 210]
})

df["feature"] = (df.sort_values(["ticker", "date"])
                 .groupby("ticker")["price"]
                 .mean()
                 .reset_index(level=0, drop= True)
)
print(df)


s = (
    df.groupby("ticker")["price"]
      .rolling(2)
      .mean().reset_index(level=0)
)

print(s)