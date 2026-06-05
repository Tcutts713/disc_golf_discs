import pandas as pd
from scipy.stats import chi2_contingency

#read file
df = pd.read_csv("disc_catalog.csv")

#clean strings
df["disc_type"] = df["disc_type"].str.strip().str.lower()
df["stability"] = df["stability"].str.strip().str.lower()

#setup data for chi test
df = df[
    df["disc_type"].notna() &
    df["stability"].notna() &
    (df["disc_type"] != "unknown") &
    (df["stability"] != "unknown") &
    (df["disc_type"] != "") &
    (df["stability"] != "")
]

contingency_table = pd.crosstab(
    df["disc_type"],
    df["stability"]
)

#chi squared test
chi2, p, dof, expected = chi2_contingency(contingency_table)

print(contingency_table)
print("Chi-square:", chi2)
print("P-value:", p)
print("Degrees of freedom:", dof)

