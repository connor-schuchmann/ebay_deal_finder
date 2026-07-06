# eBay Deal Finder

Pulls eBay listings for a search term, then analyzes them at scale to flag deals priced well below average. I built it to practice working with a REST API, paginated data collection across hundreds of results, and running statistical analysis over a large gathered set.

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

Get API keys from the eBay Developers Program, then copy `.env.example` to
`.env` and fill them in:

```
SANDBOX_CLIENT_ID=your_sandbox_client_id
SANDBOX_CLIENT_SECRET=your_sandbox_client_secret
PRODUCTION_CLIENT_ID=your_production_client_id
PRODUCTION_CLIENT_SECRET=your_production_client_secret

EBAY_ENV=PRODUCTION
```

`EBAY_ENV` toggles between PRODUCTION and SANDBOX environments. Don't commit your real `.env`.

## Usage

```
python analysis.py
```

It asks for a search term, then prints price stats and any deals it finds:

```
Search eBay for: volcom shorts
fetched: 994 items

summary (all conditions):
count    994.00
mean      25.54
std        9.84
min        2.99
25%       19.50
50%       24.50
75%       29.99
max       77.09
Name: total_price, dtype: float64

summary by condition:
                        count   mean    std    min    25%    50%    75%    max
condition
New with imperfections    6.0  23.32   3.86  16.48  22.34  24.18  25.36  27.63
New with tags           288.0  32.68  10.20   9.10  25.99  31.20  36.79  77.09
Pre-owned - Excellent   352.0  23.24   7.96   4.80  18.00  22.93  27.20  70.00
Pre-owned - Good        304.0  21.51   7.70   3.32  16.95  21.18  25.87  57.50
...

Found 132 deal(s):

Mens Volcom Khaki Drawstring Shorts Size XL
  $2.99 | Pre-owned - Fair | deal threshold: $4.28
  https://www.ebay.com/itm/198466055080

Volcom Men's Gray Cotton Chino Shorts Flat Front Pockets Button Logo
  $3.32 | Pre-owned - Good | deal threshold: $13.81
  https://www.ebay.com/itm/358729188816
...
```

## How it works

Started as a DePop scraper, but scraping a marketplace's live site runs
against its terms of service, so I rebuilt it on eBay's official Browse API
(OAuth client-credentials flow, no scraping).

- `ebay_client.py` gets access token and pulls listings, paging through
  results until it hits the total or a set cap (`MAX_ITEMS` in
  `analysis.py`, defaults to 1000).
- `listings.py` cleans the raw results — it drops accessories and parts via an `ACCESSORY_KEYWORDS` blacklist so they don't skew the numbers, and folds shipping into a true total price.
- `analysis.py` loads everything into pandas, groups by condition, and flags
  anything more than one standard deviation below its group's mean.

### Known limitation

The accessory filter is a keyword blacklist, so it's only a heuristic. For example, it might flag AirPod hooks as a "deal" when the query is AirPods. The user can add to or remove from this list manually by adding "hook" to the blacklist as a fix. A more robust solution might use category types as a filter.