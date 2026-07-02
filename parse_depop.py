from bs4 import BeautifulSoup

# opens storage for parsed data
with open("depop_raw.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

prices = soup.find_all("p", class_="styles_price__H8qdh")

prices_list = []

for price in prices:
    cost = price.get_text(strip=True)              # get dollar value
    cleaned_cost = cost.replace("$", "")           # remove $
    value = float(cleaned_cost)                    # turn to float
    prices_list.append(value)                      # add to list



