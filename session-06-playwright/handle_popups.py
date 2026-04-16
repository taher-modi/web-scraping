from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    page.goto("https://quotes.toscrape.com")
    page.wait_for_selector(".quote")

    # ── PATTERN 1: DISMISS A COOKIE BANNER ───
    # Check if a cookie accept button exists before trying to click it
    # Using is_visible() prevents errors when the element is not there
    cookie_btn = page.query_selector("button#accept-cookies")
    if cookie_btn and cookie_btn.is_visible():
        cookie_btn.click()
        print("Cookie banner dismissed.")
    else:
        print("No cookie banner found — continuing.")

    # ── PATTERN 2: SELECT FROM A DROPDOWN ────
    # page.select_option() handles <select> dropdowns by value or label
    dropdown = page.query_selector("select#category")
    if dropdown:
        page.select_option("select#category", label="Mystery")
        print("Dropdown selection made.")
    else:
        print("No dropdown found on this page — pattern noted for future use.")

    # ── PATTERN 3: WAIT FOR A SPECIFIC URL CHANGE ──
    # Useful after clicking something that triggers navigation
    print(f"\nCurrent URL: {page.url}")

    # ── PATTERN 4: TAKE A SCREENSHOT FOR DEBUGGING ──
    # When something goes wrong, a screenshot shows you exactly
    # what the browser sees at that moment — invaluable for debugging
    page.screenshot(path="debug_screenshot.png")
    print("Screenshot saved as debug_screenshot.png")
    print("Open it to see exactly what the browser was seeing.")

    browser.close()