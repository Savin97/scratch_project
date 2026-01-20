import pandas as pd

df = pd.DataFrame({
    "A":["2","3",4],
    "B": [4,6,8]
})

df = df.rename(columns= {"A":"AAA", "B":"BBB"})
print(df.head())