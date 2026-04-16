from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 10)

# ─────────────────────────────────────────
# We will simulate infinite scroll on quotes.toscrape.com/scroll
# This version of the site loads quotes as you scroll down
# ─────────────────────────────────────────

driver.get("https://quotes.toscrape.com/scroll")
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))

print("Page loaded. Starting scroll loop...\n")

collected_quotes = set()  # Use a set to automatically avoid duplicates
scroll_attempts = 0
max_scrolls = 10  # Safety limit — prevents infinite loops

while scroll_attempts < max_scrolls:
    # Get all quotes currently visible on the page
    quote_elements = driver.find_elements(By.CLASS_NAME, "quote")

    for quote in quote_elements:
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text
        collected_quotes.add((text, author))  # Tuples are hashable — sets deduplicate automatically

    print(f"Scroll {scroll_attempts + 1}: {len(collected_quotes)} unique quotes collected so far")

    # ── SCROLL DOWN ───────────────────────
    # Execute JavaScript to scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new content to load after scrolling
    time.sleep(2)

    # ── CHECK IF NEW CONTENT LOADED ───────
    new_quote_elements = driver.find_elements(By.CLASS_NAME, "quote")

    if len(new_quote_elements) == len(quote_elements):
        # Same number of quotes as before scrolling — nothing new loaded
        print("No new content loaded after scroll. Reached end of page.")
        break

    scroll_attempts += 1

driver.quit()

print(f"\nFinal count: {len(collected_quotes)} unique quotes")

# Save to CSV
import csv
with open("infinite_scroll_quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "author"])
    writer.writerows(collected_quotes)

print("Saved to infinite_scroll_quotes.csv")