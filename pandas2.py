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
merged2.to_csv("output/merged2.csv", index=False)
re_csv = pd.read_csv("output/merged2.csv")
re_csv["date"] = pd.to_datetime(re_csv['date'], errors = "coerce")
re_csv["earnings_date"] = pd.to_datetime(re_csv['earnings_date'], errors = "coerce")
merged2.to_parquet("output/merged2.parquet", index=False)
re_parq = pd.read_parquet("output/merged2.parquet")
# print(merged2.dtypes)
# print(re_csv.dtypes)
# print(re_parq.dtypes)
# print( (re_parq["price"] - merged2["price"]).abs().max() == 0 )

# Column existence
assert {"ticker", "date", "price", "earnings_date", "days_to_earnings"}.issubset(merged2.columns)

# Datatypes
assert pd.api.types.is_datetime64_any_dtype(merged2[ "date"])
assert pd.api.types.is_datetime64_any_dtype(merged2["earnings_date"])
assert pd.api.types.is_numeric_dtype(merged2["price"])

# Sorting/time intergrity 
assert merged2.groupby("ticker")["date"].is_monotonic_increasing.all()
assert not merged2.duplicated(subset=["ticker", "date"]).any()

# Merge sanity
assert merged2.shape[0] == df.shape[0]

# Range sanity
assert (merged2["price"] > 0).all()
assert (merged2["volume"] >= 0).all()



merged2= merged2.sort_values(["ticker", "date"])
merged2["ret_1d"] = merged2.groupby("ticker")["price"].pct_change()
merged2["ret_3d"] = (merged2["price"]/merged2.groupby("ticker")["price"].shift(3)) - 1
merged2["vol_10d"] = merged2.groupby("ticker")["ret_1d"].rolling(10).std().reset_index(level=0, drop=True)
vol_median = merged2.groupby("ticker")["vol_10d"].transform("median")

hot_mask = ( (merged2["days_to_earnings"].abs() <= 3) & (merged2["vol_10d"] > vol_median) )

merged2["risk_bucket"] = np.where(hot_mask, "Hot", "Normal")
sum_table = merged2.assign(is_hot =merged2["risk_bucket"]=="Hot" ).groupby("ticker").agg(
    vol_mean = ("vol_10d", "mean"),
    hot_percentage = ("is_hot", "mean"),
    row_count = ("price", "size")
)
sum_table = sum_table.reset_index()

hot = (merged2["days_to_earnings"] <= 3) & (merged2["vol_10d"] > merged2.groupby("ticker")["vol_10d"].transform("median"))
merged2["risk_bucket"] = np.where(hot, "hot", "normal")

print(merged2.groupby("ticker")["vol_10d"].median())
print("--------------------")

print(merged2.groupby("ticker")["vol_10d"].transform("median"))



#print(merged2.head())
print("--------------------")
print("Done.")

