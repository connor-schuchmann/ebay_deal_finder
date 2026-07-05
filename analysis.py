import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")  # Windows console defaults cp1252, utf-8 covers all characters

from ebay_client import get_access_token, search_all_listings
from listings import extract_listings

query = "airpods pro 2nd gen"  # what we are searching for

token = get_access_token()
items = search_all_listings(token, query)
data = extract_listings(items)

print(f"fetched: {len(items)} items\n")

# push data to panda + show stats
df = pd.DataFrame(data)
df["condition"] = df["condition"].fillna("Unknown")  # replaces every NaN with "Unknown"

print("summary (all conditions): ")
print(df["total_price"].describe().round(2))

print("\nsummary by condition: ")
print(df.groupby("condition")["total_price"].describe().round(2))

# sort by condition
deal_groups = []

for condition, group in df.groupby("condition"): # loops for all conditions by amount group (dependent on condtion)
    if len(group) < 3:
        continue  # too few listings to be significant

    mean = group["total_price"].mean()
    std = group["total_price"].std()
    threshold = mean - std

    condition_deals = group[group["total_price"] < threshold].copy()  # guard against modifying original df
    condition_deals["threshold"] = round(threshold, 2) # creates "threshold" in pd
    deal_groups.append(condition_deals) # adds to deal_groups

if deal_groups: # if ANY deals
    deals = pd.concat(deal_groups).sort_values("total_price") # combines pd for all conditions to deals
else: # if NO deals
    deals = pd.DataFrame(columns=["title", "total_price", "condition", "threshold", "url"])

# show deals
print(f"\nFound {len(deals)} deal(s):\n")
print(deals[["title", "total_price", "condition", "threshold", "url"]].to_string(index=False))