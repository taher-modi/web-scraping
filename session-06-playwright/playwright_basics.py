from playwright.sync_api import sync_playwright

# ─────────────────────────────────────────
# Playwright uses a context manager pattern
# Everything runs inside the "with sync_playwright() as p" block
# ─────────────────────────────────────────

with sync_playwright() as p:

    # STEP 1: LAUNCH BROWSER
    # headless=True = runs invisibly
    # headless=False = opens a visible window (useful for debugging)
    browser = p.chromium.launch(headless=True)

    # STEP 2: CREATE A BROWSER CONTEXT
    # A context is like a fresh browser profile — clean cookies, clean state
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080}
    )

    # STEP 3: OPEN A NEW PAGE (TAB)
    page = context.new_page()

    # STEP 4: NAVIGATE TO THE TARGET
    page.goto("https://quotes.toscrape.com/js/")

    # STEP 5: WAIT FOR CONTENT
    # wait_for_selector waits until the element appears in the DOM
    # No need to create a separate Wait object like in Selenium
    page.wait_for_selector(".quote")

    print(f"Page title: {page.title()}")

    # STEP 6: EXTRACT DATA
    # query_selector_all finds all matching elements
    quotes = page.query_selector_all(".quote")
    print(f"Found {len(quotes)} quotes\n")

    for quote in quotes:
        text = quote.query_selector(".text").inner_text()
        author = quote.query_selector(".author").inner_text()
        print(f"{author}: {text}")

    # STEP 7: ALWAYS CLOSE
    browser.close()

print("\nDone.")