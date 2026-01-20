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

df_for_merging = pd.DataFrame({
    "earnings_date": np.repeat(pd.date_range("2024-02-01", periods=40, freq="D"), len(tickers)),
    "ticker": tickers * len(dates),
    "EPS": np.random.uniform( 10,90, size = len(dates) * len(tickers)).round(2) 
})
#df_for_merging = df_for_merging.sort_values(["ticker","earnings_date"])

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
#df.to_csv("output/pandas2.csv", index=False)

df["date"] = pd.to_datetime( df["date"] )
df = df.sort_values(["ticker", "date"]).reset_index(drop = True)
df = df.set_index(["ticker", "date"]).sort_index()

aapl_slice = df.loc[  ( "AAPL", slice("2024-01-20", "2024-01-10") ), :  ]
df = df.reset_index()

df = df.set_index(["ticker", "date"])
df = df.sort_values(["ticker", "date"]).reset_index()

rets = df.groupby("ticker")["price"].pct_change()
vol = rets.groupby(df["ticker"]).std()

top_ticker = vol.idxmax()
top_vol = vol.loc[top_ticker]

sum_table = df.groupby("ticker").agg(
    mean_price = ("price", "mean"),
    max_price = ("price", "max"),
    obs_count = ("price", "size")
)

df["ticker_mean_price"] = df.groupby("ticker")["price"].transform("mean")
df["above_mean"] = df["price"] > df["ticker_mean_price"]
rets = df.groupby("ticker")["price"].pct_change()
vol = df.groupby("ticker")["price"].pct_change().std()

df["rolling_5_mean"] = (
                df.groupby("ticker")["price"]
                .rolling(5)
                .mean()
                .reset_index(level=0, drop=True)
        )
# Valid alternative using transform is:
df["rolling_mean_5"] = (
    df.groupby("ticker")["price"]
        .transform(lambda x: x.rolling(5).mean())
)


df["rolling_10_vol"] = (
    df.groupby("ticker")["return"]
    .rolling(10)
    .std()
    .reset_index(level=0, drop=True)
)   

#print(df[["price_diff", "return", "next_price", "rolling_5_mean", "rolling_10_vol"]].isna().sum())
df_model = df.copy().dropna(subset=["return","rolling_10_vol"])
df["price_diff"] = df["price_diff"].fillna(0)
assert df_model[["return", "rolling_10_vol"]].isna().sum().sum() == 0

merged = df.merge(df_for_merging, left_on=["ticker","date"], right_on=["ticker", "earnings_date"], how="left")
merged = merged.sort_values(["ticker","date"])

merged.to_csv("output/merged.csv", index = False)

earnings = pd.DataFrame({
    "ticker": ["AAPL", "MSFT", "GOOGL", "AMZN"],
    "earnings_date": pd.to_datetime(["2024-01-15", "2024-01-18", "2024-01-22", "2024-01-25"]),
    "eps_est": [2.1, 1.9, 1.2, 0.8],
})
merged2 = df.merge(earnings, on="ticker", how="left", validate="many_to_one")
assert df.shape[0] == merged2.shape[0]

merged2["days_to_earnings"] = (merged2["earnings_date"] - merged2["date"]).dt.days



sector_map = {"AAPL": "tech", "MSFT": "tech", "GOOGL": "tech", "AMZN": "consumer"}

merged2["sector"] = merged2["ticker"].map(sector_map)



merged2 = merged2.drop(columns=["dollar_volume","price_diff","market"])


merged2["abs_days"] = merged2["days_to_earnings"].abs()
sector_map = {"AAPL": "tech", "MSFT": "tech", "GOOGL": "tech", "AMZN": "consumer"}
merged2["sector"] = merged2["ticker"].map(sector_map)
def label_days(d):
    if d <0:
        return "after"
    if d<=3:
        return "imminent"
    if d<=10:
        return "soon"
    return "far"
merged2["earnings_bucket"] = merged2["days_to_earnings"].apply(label_days)

value_counts = merged2["earnings_bucket"].value_counts()
print("\n--------------------\n")

print(value_counts)





#print(merged2.head())
print("--------------------")
df.to_csv("output/df.csv", index=False)
df_for_merging.to_csv("output/df_for_merging.csv", index=False)
print("Done.")
