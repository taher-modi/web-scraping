from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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

all_quotes = []
page = 1

print("Starting paginated scrape of JS quotes site...\n")

driver.get("https://quotes.toscrape.com/js/")

while True:
    # Wait for quotes to load on the current page
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))

    quotes = driver.find_elements(By.CLASS_NAME, "quote")

    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text
        tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]

        all_quotes.append({
            "text": text,
            "author": author,
            "tags": ", ".join(tags),
            "page": page
        })

    print(f"Page {page}: scraped {len(quotes)} quotes")

    # ── CHECK FOR NEXT BUTTON ─────────────
    # Try to find the Next button — if it does not exist we are on the last page
    try:
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
        next_button.click()  # Click it to go to the next page
        page += 1

    except:
        # No Next button found — we have reached the last page
        print("No more pages found.")
        break

driver.quit()

print(f"\nTotal quotes scraped: {len(all_quotes)}")

# Save to CSV
import csv
with open("js_quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags", "page"])
    writer.writeheader()
    writer.writerows(all_quotes)

print("Saved to js_quotes.csv")