from ebay_client import get_access_token, search_all_listings


def extract_listings(listings_raw):  # sorts paginated listings
    listings = []

    for listing_raw in listings_raw:
        price = float(listing_raw["price"]["value"])

        shipping_options = listing_raw.get("shippingOptions", []) # items may have cheaper prices but equivalent costs considering shipping
        if shipping_options:
            shipping_cost = shipping_options[0].get("shippingCost")             # included when cost is FIXED
            shipping = float(shipping_cost["value"]) if shipping_cost else 0.0  # included when cost is DYNAMIC
        else:
            shipping = 0.0  # no shipping info listed

        listing = {
            "title": listing_raw.get("title"),
            "price": price,
            "shipping": shipping,
            "total_price": price + shipping,    # true cost
            "condition": listing_raw.get("condition"),
            "url": listing_raw.get("itemWebUrl"),
        }

        listings.append(listing)

    return listings


if __name__ == "__main__":
    # confirm token
    token = get_access_token()

    # confirm search
    items = search_all_listings(token, "nike shirt")
    print(f"fetched: {len(items)} items")

    # confirm extraction
    cleaned = extract_listings(items)
    print(f"Extracted {len(cleaned)} listings")

    for listing in cleaned[:5]:
        print(listing)
