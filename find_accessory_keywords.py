import re
import statistics
import sys
from collections import defaultdict

from ebay_client import get_access_token, search_all_listings
from listings import extract_listings

sys.stdout.reconfigure(encoding="utf-8")  # cover all characters

MAX_ITEMS = 1000
MIN_OCCURRENCES = 5    # ignore rare words
RATIO_THRESHOLD = 0.5  # increase for less strict, decrease for more strict

STOPWORDS = {"a", "an", "and", "the", "for", "with", "of", "in", "on", "new", "used"}

def tokenize(title):
    # r"..." = raw string
    # [a-z0-9] = match any single lowercase letter or digit
    words = re.findall(r"[a-z0-9]+", title.lower())

    result = [] # create list of words
    for word in words:
        if len(word) > 2 and word not in STOPWORDS:
            result.append(word)
    return result


query = input("Search eBay for: ")
query_words = set(tokenize(query))  # tokenize() query term; ex] "airpods max 2" -> {"airpods", "max"}

# search eBay
token = get_access_token()
items = search_all_listings(token, query, max_items=MAX_ITEMS)
data = extract_listings(items, query)

# data failure
if not data:
    print("No listings found for that search. Try a different query.")
    sys.exit()

all_prices = [listing["total_price"] for listing in data]  # pull total_price out of every listing dict
overall_median = statistics.median(all_prices)

prices_by_word = defaultdict(list)

for listing in data:

    words = set(tokenize(listing["title"])) - query_words # filter query word from descriptive words

    for word in words:
        
        prices_by_word[word].append(listing["total_price"]) # associate cost with each descriptor

#stored as tuple
results = []
for word, prices in prices_by_word.items():
    if len(prices) < MIN_OCCURRENCES:        # exclude rare words
        continue

    word_median = statistics.median(prices)        # median price per word
    ratio = word_median / overall_median
    if ratio <= RATIO_THRESHOLD:                   # keep notably cheap words
        results.append((ratio, word, len(prices), word_median))  # store as a tuple

results.sort()  # sorts tuples by their first element (ratio); cheapest first

# print data for human interperetation
print(f"\n{len(data)} listings, overall median price: ${overall_median:.2f}\n")
print(f"{'word':<20} {'count':>6} {'median $':>10} {'ratio':>7}") # headers
for ratio, word, count, word_median in results:  # actual values for all results
    print(f"{word:<20} {count:>6} {word_median:>10.2f} {ratio:>7.2f}")

# format for convenience
if results:
    print("\nreview and add to ACCESSORY_KEYWORDS:")
    words = ", ".join(f'"{word}"' for _, word, _, _ in results)
    print(words)
