from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ─────────────────────────────────────────
# STEP 1: CONFIGURE CHROME OPTIONS
# ─────────────────────────────────────────

options = Options()

# Headless mode = Chrome runs invisibly in the background without opening a window
# Comment this line out if you want to WATCH the browser work (useful for debugging)
options.add_argument("--headless")

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

# Make Chrome look like a real browser — not a bot
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")


# ─────────────────────────────────────────
# STEP 2: LAUNCH THE BROWSER
# webdriver-manager handles downloading the right ChromeDriver automatically
# ─────────────────────────────────────────

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

print("Browser launched successfully.")


# ─────────────────────────────────────────
# STEP 3: NAVIGATE TO A PAGE
# ─────────────────────────────────────────

driver.get("https://quotes.toscrape.com/js/")
# This is the JavaScript version of the quotes site
# Plain requests returns empty content here — Selenium handles it fine

print(f"Page title: {driver.title}")
print(f"Current URL: {driver.current_url}")


# ─────────────────────────────────────────
# STEP 4: WAIT FOR CONTENT TO LOAD
# NEVER use time.sleep() to wait for elements — it is unreliable
# Use WebDriverWait with expected_conditions instead
# This waits UP TO 10 seconds for the element to appear, then proceeds
# ─────────────────────────────────────────

wait = WebDriverWait(driver, 10)

# Wait until at least one quote div is present in the DOM
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))

print("Quotes loaded successfully.")


# ─────────────────────────────────────────
# STEP 5: FIND AND EXTRACT ELEMENTS
# By.CLASS_NAME, By.ID, By.CSS_SELECTOR, By.XPATH are the main locators
# ─────────────────────────────────────────

quotes = driver.find_elements(By.CLASS_NAME, "quote")
print(f"Found {len(quotes)} quotes on this page.")

for quote in quotes:
    text = quote.find_element(By.CLASS_NAME, "text").text
    author = quote.find_element(By.CLASS_NAME, "author").text
    print(f"\n{author}: {text}")


# ─────────────────────────────────────────
# STEP 6: ALWAYS CLOSE THE BROWSER WHEN DONE
# If you forget this, Chrome processes pile up in the background
# ─────────────────────────────────────────

driver.quit()
print("\nBrowser closed.")