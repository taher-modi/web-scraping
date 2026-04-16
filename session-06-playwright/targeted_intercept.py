from playwright.sync_api import sync_playwright
import json
import csv

all_quotes = []

def handle_response(response):
    print(response.url)
    # Only process responses from the quotes API endpoint
    if "/api/quotes" in response.url and response.status == 200:
        try:
            data = response.json()
            quotes = data.get("quotes", [])

            for quote in quotes:
                all_quotes.append({
                    "text": quote.get("text", ""),
                    "author": quote.get("author", {}).get("name", ""),
                    "tags": ", ".join(quote.get("tags", []))
                })

            print(f"Captured {len(quotes)} quotes from: {response.url}")
        except Exception as e:
            print(f"Parse error: {e}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    page.on("response", handle_response)

    # ── PAGINATE BY CLICKING NEXT ─────────
    page.goto("https://quotes.toscrape.com/js/")
    page.wait_for_selector(".quote")

    while True:
        # Wait for network to settle after each page load
        page.wait_for_load_state("networkidle")

        # Check if Next button exists
        next_btn = page.query_selector("li.next a")
        if not next_btn:
            print("No more pages.")
            break

        next_btn.click()
        page.wait_for_selector(".quote")

    browser.close()

print(f"\nTotal quotes collected via interception: {len(all_quotes)}")

# Export to CSV
with open("intercepted_quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(all_quotes)

print("Saved to intercepted_quotes.csv")