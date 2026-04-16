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

# ─────────────────────────────────────────
# quotes.toscrape.com has a login page for practice
# Credentials: username = "admin", password = "12345"
# ─────────────────────────────────────────

driver.get("https://quotes.toscrape.com/login")

# Wait for the form to appear
wait.until(EC.presence_of_element_located((By.ID, "username")))

# Find the username field and type into it
username_field = driver.find_element(By.ID, "username")
username_field.clear()  # Clear any pre-filled content first
username_field.send_keys("admin")

# Find the password field and type into it
password_field = driver.find_element(By.ID, "password")
password_field.clear()
password_field.send_keys("12345")

print("Form filled. Submitting...")

# Find and click the submit button
submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
submit_button.click()

# Wait for the page to change after login
wait.until(EC.url_changes("https://quotes.toscrape.com/login"))

print(f"After login, current URL: {driver.current_url}")

# Check if login succeeded by looking for the logout link
try:
    driver.find_element(By.XPATH, "//a[contains(text(), 'Logout')]")
    print("Login successful — Logout link found on page.")
except:
    print("Login may have failed — Logout link not found.")

# Now scrape quotes as a logged-in user
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))
quotes = driver.find_elements(By.CLASS_NAME, "quote")
print(f"\nScraped {len(quotes)} quotes after logging in.")

driver.quit()
print("Done.")