import pandas as pd

table = pd.read_csv("eco2.csv", index_col=0)

print(len(table))