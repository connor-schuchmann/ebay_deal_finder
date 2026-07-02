import re
from bs4 import BeautifulSoup

# open the saved HTML and parse it
with open("depop_raw.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# find all listing cards — one entry per item
listings = soup.find_all("div", class_=re.compile(r"productCardRoot"))

prices_list = []

for listing in listings:
    # grab the actual (discount) price, NOT the strikethrough original
    price = listing.find("p", class_=re.compile(r"styles_price__"))

    if price is None:
        continue   # this card has no price, skip it

    cost = price.get_text(strip=True)      # e.g. "$22.09"
    cleaned_cost = cost.replace("$", "")   # remove $
    value = float(cleaned_cost)            # turn to float
    prices_list.append(value)

print("listings found:", len(listings))
print("prices extracted:", len(prices_list))
print(prices_list)