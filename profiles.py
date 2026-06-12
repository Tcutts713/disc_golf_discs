import pandas as pd

df = pd.read_csv("disc_catalog.csv")

stability_counts = pd.crosstab(
    df["manufacturer"],
    df["stability"]
)

stability_pct = (
    stability_counts
    .div(stability_counts.sum(axis=1), axis=0)
    .multiply(100)
    .round(2)
)

# Rename columns to make them clear
stability_pct.columns = [
    f"{col}_pct" for col in stability_pct.columns
]

disctype_counts = pd.crosstab(
    df["manufacturer"],
    df["disc_type"]
)

disctype_pct = (
    disctype_counts
    .div(disctype_counts.sum(axis=1), axis=0)
    .multiply(100)
    .round(2)
)

# Rename columns
disctype_pct.columns = [
    f"{col}_pct" for col in disctype_pct.columns
]

mold_counts = (
    df.groupby("manufacturer")
      .size()
      .rename("total_molds")
)

manufacturer_profiles = pd.concat(
    [mold_counts, stability_pct, disctype_pct],
    axis=1
).reset_index()

# Sort by number of molds
manufacturer_profiles = manufacturer_profiles.sort_values(
    by="total_molds",
    ascending=False
)

manufacturer_profiles.to_csv(
    "manufacturer_fingerprint_profiles.csv",
    index=False
)

print("Export complete.")
print(manufacturer_profiles.head())