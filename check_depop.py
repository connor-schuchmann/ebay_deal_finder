import requests

URL = "https://www.depop.com/search/?q=volcom%20shorts"

# Mimic a real browser to avoid a quick 403 block
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(URL, headers=HEADERS, timeout=15)

# Save the raw HTML for inspection
with open("depop_raw.html", "w", encoding="utf-8") as f:
    f.write(response.text)

has_volcom = "volcom" in response.text.lower()

print(f"Status code : {response.status_code}")
print(f"HTML length : {len(response.text):,} chars")
print(f"'volcom' found: {has_volcom}")
