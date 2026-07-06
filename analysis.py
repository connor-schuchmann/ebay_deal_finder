import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")                            # Windows console defaults cp1252, utf-8 covers all characters

from ebay_client import get_access_token, search_all_listings
from listings import extract_listings

MAX_ITEMS = 1000                                                     # cap on how many listings to pull per search

query = input("Search eBay for: ")                                   # search prompt

token = get_access_token()
items = search_all_listings(token, query, max_items=MAX_ITEMS)
data = extract_listings(items)

print(f"fetched: {len(items)} items\n")


if not data:                                                         # failure guard when no listings
    print("No listings found for that search. Try a different query.")
    sys.exit()

# push data to panda + show stats
df = pd.DataFrame(data)
df["condition"] = df["condition"].fillna("Unknown")                  # replaces every NaN with "Unknown"

print("summary (all conditions): ")
print(df["total_price"].describe().round(2))

print("\nsummary by condition: ")
print(df.groupby("condition")["total_price"].describe().round(2))

# sort by condition
deal_groups = []

for condition, group in df.groupby("condition"):                     # loops for all conditions by amount group (dependent on condtion)
    if len(group) < 3:
        continue                                                     # too few listings to be significant

    mean = group["total_price"].mean()
    std = group["total_price"].std()
    threshold = mean - std

    condition_deals = group[group["total_price"] < threshold].copy() # guard against modifying original df
    condition_deals["threshold"] = round(threshold, 2)               # creates "threshold" in pd
    deal_groups.append(condition_deals)                              # adds to deal_groups

if deal_groups:                                                      # if ANY deals
    deals = pd.concat(deal_groups).sort_values("total_price")        # combines pd for all conditions to deals
else:                                                                # if NO deals
    deals = pd.DataFrame(columns=["title", "total_price", "condition", "threshold", "url"])

                                                                     # show deals, one per block so long titles/urls don't wrap into each other
print(f"\nFound {len(deals)} deal(s):\n")

for _, deal in deals.iterrows():                                     # .iterrows() gives (index, row) pairs; we only need the row
    print(deal["title"])
    print(f"  ${deal['total_price']:.2f} | {deal['condition']} | deal threshold: ${deal['threshold']:.2f}")
    print(f"  {deal['url']}\n")