ACCESSORY_KEYWORDS = [                                                         # titles containing these are parts/accessories, not the actual product
    "case", "cover", "tips", "tip", "skin", "sticker", "strap",
    "empty box", "box only", "for parts", "replacement", "manual", "packaging",
]


def is_accessory(title, query=""):
    title = title.lower()
    query = query.lower()
    return any(keyword in title and keyword not in query for keyword in ACCESSORY_KEYWORDS)
