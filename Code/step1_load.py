import pandas as pd

df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding="latin-1")

print("Shape:", df.shape)
print("\nColumns:\n", df.columns.tolist())
print("\nMissing values:\n", df.isnull().sum()[df.isnull().sum() > 0])
print("\nSample row:\n", df.iloc[0])