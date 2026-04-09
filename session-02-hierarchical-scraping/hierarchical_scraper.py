import requests
import csv
import time
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com"


# ─────────────────────────────────────────
# HELPER FUNCTION
# Used by every level — fetches a URL and returns a soup object
# ─────────────────────────────────────────
def get_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"  WARNING: Failed to fetch {url} — status {response.status_code}")
        return None
    return BeautifulSoup(response.text, "html.parser")


# ─────────────────────────────────────────
# LEVEL 1: Get all category names and URLs
# ─────────────────────────────────────────
def get_categories():
    print("Fetching category list...")
    soup = get_soup(BASE_URL)

    # The category list is inside a <ul class="nav-list"> then a nested <ul>
    category_section = soup.find("ul", class_="nav-list").find("ul")

    categories = []
    for li in category_section.find_all("li"):
        a = li.find("a")
        name = a.get_text(strip=True)
        # a["href"] looks like "catalogue/category/books/mystery_3/index.html"
        link = BASE_URL + "/" + a["href"]
        categories.append({"name": name, "url": link})

    print(f"Found {len(categories)} categories")
    return categories


# ─────────────────────────────────────────
# LEVEL 2: Get all book detail URLs from a category page
# Handles pagination within a category
# ─────────────────────────────────────────
def get_book_urls_from_category(category_url, category_name):
    book_urls = []
    url = category_url

    while url:
        soup = get_soup(url)
        if not soup:
            break

        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            relative_link = article.find("a")["href"]
            # relative_link looks like "../../a-light-in-the-attic_1000/index.html"
            # We strip out the "../" parts and build the correct absolute URL
            clean_link = BASE_URL + "/catalogue/" + relative_link.replace("../", "")
            book_urls.append(clean_link)

        # Check if there is a Next button for pagination inside this category
        next_btn = soup.find("li", class_="next")
        if next_btn:
            next_href = next_btn.find("a")["href"]
            # Build next page URL relative to the current category URL
            url = category_url.rsplit("/", 1)[0] + "/" + next_href
        else:
            url = None  # No more pages in this category

    return book_urls


# ─────────────────────────────────────────
# LEVEL 3: Scrape detail data from one book's page
# ─────────────────────────────────────────
def get_book_details(book_url, category):
    soup = get_soup(book_url)
    if not soup:
        return None

    title = soup.find("h1").get_text(strip=True)

    # Rating is stored as a word in the CSS class, e.g. class="star-rating Three"
    rating_tag = soup.find("p", class_="star-rating")
    rating = rating_tag["class"][1]  # Gets "One", "Two", "Three" etc.

    price = soup.find("p", class_="price_color").get_text(strip=True)

    availability = soup.find("p", class_="instock availability").get_text(strip=True)

    # Not every book has a description
    desc_tag = soup.find("div", id="product_description")
    if desc_tag:
        description = desc_tag.find_next_sibling("p").get_text(strip=True)
    else:
        description = "N/A"

    return {
        "title": title,
        "category": category,
        "rating": rating,
        "price": price,
        "availability": availability,
        "description": description[:200],
        "url": book_url
    }


# ─────────────────────────────────────────
# MAIN: Wire all three levels together
# ─────────────────────────────────────────
all_books_data = []

categories = get_categories()

# Scraping all 50 categories takes a while — start with 3 to test
for category in categories:
    print(f"\nCategory: {category['name']}")

    book_urls = get_book_urls_from_category(category["url"], category["name"])
    print(f"  Found {len(book_urls)} books")

    for i, book_url in enumerate(book_urls):
        details = get_book_details(book_url, category["name"])

        if details:
            all_books_data.append(details)

        # Small delay between requests — polite scraping avoids getting blocked
        time.sleep(0.3)

        if (i + 1) % 5 == 0:
            print(f"  Progress: {i + 1}/{len(book_urls)} books scraped")

# Save everything to CSV
with open("books_data.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["title", "category", "rating", "price", "availability", "description", "url"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_books_data)

print(f"\nDone. Scraped {len(all_books_data)} books total.")
print("Data saved to books_data.csv")