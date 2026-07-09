import re
import statistics
import sys
from collections import defaultdict

from ebay_client import get_access_token, search_all_listings
from listings import extract_listings

sys.stdout.reconfigure(encoding="utf-8")  # cover all characters

MAX_ITEMS = 1000
MIN_OCCURRENCES = 5    # ignore rare words
RATIO_THRESHOLD = 0.5

STOPWORDS = {"a", "an", "and", "the", "for", "with", "of", "in", "on", "new", "used"}

def tokenize(title):
    # r"..." = raw string
    # [a-z0-9] = match any single lowercase letter or digit
    words = re.findall(r"[a-z0-9]+", title.lower())

    result = [] # create list of words
    for w in words:
        if len(w) > 2 and w not in STOPWORDS:
            result.append(w)
    return result


query = input("Search eBay for: ")
query_words = set(tokenize(query))  # tokenize() query term; ex] "airpods max 2" -> {"airpods", "max"}

token = get_access_token()
items = search_all_listings(token, query, max_items=MAX_ITEMS)
data = extract_listings(items)

if not data:
    print("No listings found for that search. Try a different query.")
    sys.exit()

all_prices = [listing["total_price"] for listing in data]  # pull total_price out of every listing dict
overall_median = statistics.median(all_prices)

prices_by_word = defaultdict(list)

for listing in data:

    words = set(tokenize(listing["title"])) - query_words

    for word in words:
        
        prices_by_word[word].append(listing["total_price"])

results = []
for word, prices in prices_by_word.items():
    if len(prices) < MIN_OCCURRENCES:        # not enough listings with this word to trust its median
        continue

    word_median = statistics.median(prices)        # median price per word
    ratio = word_median / overall_median
    if ratio <= RATIO_THRESHOLD:                   # keep notably cheap words
        results.append((ratio, word, len(prices), word_median))  # store as a tuple of 4 values

results.sort()  # sorts tuples by their first element (ratio); cheapest first

print(f"\n{len(data)} listings, overall median price: ${overall_median:.2f}\n")
print(f"{'word':<20} {'count':>6} {'median $':>10} {'ratio':>7}")  # <20/>6 etc = column width + left/right align
for ratio, word, count, word_median in results:  # unpacking: pulls each tuple's 4 values back into named variables
    print(f"{word:<20} {count:>6} {word_median:>10.2f} {ratio:>7.2f}")

if results:
    print("\nreview and add to ACCESSORY_KEYWORDS):")
    words = ", ".join(f'"{word}"' for _, word, _, _ in results)
    print(words)
