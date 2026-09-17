import pandas as pd

data = pd.read_csv("dataset/placement.csv")

print(data.head())

print("\n----------------------------------")

# Show column names
print("Columns:")
print(data.columns)

print("\n----------------------------------")

# Show dataset information
print("Dataset Info:")
print(data.info())

print("\n----------------------------------")

# Show missing values
print("Missing Values:")
print(data.isnull().sum())