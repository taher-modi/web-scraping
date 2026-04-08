import requests
import csv
from bs4 import BeautifulSoup

base_url = "https://quotes.toscrape.com"
all_quotes = []
page = 1

while True:
    url = f"{base_url}/page/{page}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    # If no quotes found, we have gone past the last page
    if not quotes:
        print(f"No more pages. Stopped at page {page}.")
        break

    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

        all_quotes.append({
            "text": text,
            "author": author,
            "tags": ", ".join(tags)
        })

    print(f"Scraped page {page} — {len(quotes)} quotes found")
    page += 1

print(f"\nTotal quotes scraped: {len(all_quotes)}")

import csv

with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(all_quotes)

print("Data saved to quotes.csv")