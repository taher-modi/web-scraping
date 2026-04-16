from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36"
]

def get_driver(headless=True, proxy=None):
    """
    Returns a configured Selenium WebDriver instance.

    headless: True = runs invisibly, False = opens a visible browser window
    proxy: Pass proxy string like "http://user:pass@host:port" or None
    """
    options = Options()

    if headless:
        options.add_argument("--headless")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

    # Plug in proxy if provided — same concept as requests proxies
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver


def get_wait(driver, timeout=10):
    """Returns a WebDriverWait object for the given driver."""
    return WebDriverWait(driver, timeout)


# ── TEST THE UTILITY ─────────────────────
if __name__ == "__main__":
    driver = get_driver(headless=True)
    wait = get_wait(driver)

    driver.get("https://quotes.toscrape.com")
    print(f"Page title: {driver.title}")
    print("Reusable driver setup working correctly.")

    driver.quit()