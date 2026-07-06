ACCESSORY_KEYWORDS = [                                                         # titles containing these are parts/accessories, not the actual product
    "case", "cover", "tips", "tip", "skin", "sticker", "strap",
    "empty box", "box only", "for parts", "replacement", "manual", "packaging",
]


def is_accessory(title):
    title = title.lower()
    return any(keyword in title for keyword in ACCESSORY_KEYWORDS)


def extract_listings(listings_raw):                                             # sorts paginated listings
    listings = []

    for listing_raw in listings_raw:
        title = listing_raw.get("title", "")
        if is_accessory(title):                                                 # skip accessories/parts so they don't skew the sample set
            continue

        price = float(listing_raw["price"]["value"])

        shipping_options = listing_raw.get("shippingOptions", [])               # items may have cheaper prices but equivalent costs considering shipping
        if shipping_options:
            shipping_cost = shipping_options[0].get("shippingCost")             # included when cost is FIXED
            shipping = float(shipping_cost["value"]) if shipping_cost else 0.0  # included when cost is DYNAMIC
        else:
            shipping = 0.0                                                      # no shipping info listed

        url = listing_raw.get("itemWebUrl", "")
        url = url.split("?")[0]                                                 # drop eBay's tracking query params

        listing = {
            "title": title,
            "price": price,
            "shipping": shipping,
            "total_price": price + shipping,                                    # true cost
            "condition": listing_raw.get("condition"),
            "url": url,
        }

        listings.append(listing)

    return listings
