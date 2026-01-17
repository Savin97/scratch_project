import pandas as pd
import numpy as np

np.random.seed(42)

pd.set_option("display.width", 50)
pd.set_option("display.max_rows", 30)

dates = pd.date_range("2024-01-01", periods=40, freq="D")
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
print("\n\n\n")
df = pd.DataFrame({
    "date": np.repeat(dates, len(tickers)),
    "ticker": tickers * len(dates),
    "price": np.random.uniform(100, 300, size=len(dates) * len(tickers)).round(2),
    "volume": np.random.randint(1_000, 20_000, size=len(dates) * len(tickers))
})

df["market"] = ["US"] * len(df)
df["dollar_volume"] = (df["price"] * df["volume"]).round(2)

df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

df.index = df["price"]
# print(df.iloc[0:5, 0:4])
df.reset_index(drop=True, inplace=True)
# print(df["price"] == 174.91)

# print(df[ ["price", "market"] ])

df2 = df[ ["date", "ticker"] ].copy()

#df["return"] = df["price"].pct_change() # Wrong for multiple tickers

df["price_diff"] = df.groupby("ticker")["price"].diff()

df["return"] = df.groupby("ticker")["price"].pct_change()

df["next_price"] = df.groupby("ticker")["price"].shift(-1)

df['log_return'] = np.log(df["price"]/ df.groupby("ticker")["price"].shift(1))

df.sort_values(["ticker", "date"])
#df.to_csv("pandas2.csv", index=False)

df["date"] = pd.to_datetime( df["date"] )
df = df.sort_values(["ticker", "date"]).reset_index(drop = True)
df = df.set_index(["ticker", "date"]).sort_index()

aapl_slice = df.loc[  ( "AAPL", slice("2024-01-20", "2024-01-10") ), :  ]


df = df.reset_index()

df = df.set_index(["ticker", "date"])
df = df.sort_values(["ticker", "date"]).reset_index()
print(df)
print("--------------------\n")


rets = df.groupby("ticker")["price"].pct_change()
vol = rets.groupby(df["ticker"]).std()


sum_table = df.groupby("ticker").agg(
    mean_price = ("price", "mean"),
    max_price = ("price", "max"),
    obs_count = ("price", "size")
)

df["ticker_mean_price"] = df.groupby("ticker")["price"].transform("mean")
df["above_mean"] = df["price"] > df["ticker_mean_price"]

rets = df.groupby("ticker")["price"].pct_change()

vol = df.groupby("ticker")["price"].pct_change().std()

print(vol)

top_ticker = vol.idxmax()
top_vol = vol.loc[top_ticker]

print(f"{top_ticker}: {top_vol:.4f}")
print("--------------------")
print("Done.")


