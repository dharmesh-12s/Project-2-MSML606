import pandas as pd

df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding="latin-1")

# Drop useless columns
drop_cols = [
    'Customer Email', 'Customer Password', 'Customer Fname', 'Customer Lname',
    'Customer Street', 'Customer Zipcode', 'Order Zipcode',
    'Product Description', 'Product Image'
]
df.drop(columns=drop_cols, inplace=True)

# Parse dates
df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
df['shipping date (DateOrders)'] = pd.to_datetime(df['shipping date (DateOrders)'])

# Keep only completed/closed orders
df = df[df['Order Status'].isin(['COMPLETE', 'CLOSED'])]

# Columns we'll use for graph construction
graph_cols = [
    'Order Region', 'Order Country', 'Order City',
    'Shipping Mode', 'Days for shipping (real)', 'Days for shipment (scheduled)',
    'Order Item Total', 'Order Profit Per Order', 'Late_delivery_risk',
    'Delivery Status', 'Market', 'Department Name', 'Product Name'
]
df_clean = df[graph_cols].dropna()

print("Clean shape:", df_clean.shape)
print("\nShipping Modes:", df_clean['Shipping Mode'].unique())
print("\nMarkets:", df_clean['Market'].unique())
print("\nSample:\n", df_clean.head(3))

df_clean.to_csv("supply_chain_clean.csv", index=False)
print("\nSaved: supply_chain_clean.csv")