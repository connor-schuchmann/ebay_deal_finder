import re
from bs4 import BeautifulSoup

with open("depop_raw.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

listings = soup.find_all("div", class_=re.compile(r"productCardRoot"))  # get every <div> in product card

data = []

for listing in listings:
    # brand
    brand = listing.find("p", class_=re.compile(r"brandName"))
    brand_text = brand.get_text(strip=True) if brand else "N/A"

    # size
    size = listing.find("p", class_=re.compile(r"sizeAttributeText"))
    size_text = size.get_text(strip=True) if size else "N/A"

    # price (check for discsount)
    price = listing.find("p", attrs={"aria-description": "Discounted price"})
    if price is None:
        price = listing.find("p", attrs={"aria-description": "Price with fee"})
    if price is None:
        price = listing.find("p", class_=re.compile(r"styles_price__"))

    if price is None:
        price_value = "N/A"
    else:
        cost = price.get_text(strip=True).replace("$", "")
        price_value = float(cost)

    # url
    link = listing.find("a", class_=re.compile(r"unstyledLink"))
    url = "https://www.depop.com" + link["href"] if link else "N/A"

    data.append({
        "brand": brand_text,
        "size": size_text,
        "price": price_value,
        "url": url,
    })

