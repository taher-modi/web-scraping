from playwright.sync_api import sync_playwright
import json

# ─────────────────────────────────────────
# We will intercept all network requests made by the browser
# and capture any that return JSON data
# ─────────────────────────────────────────

captured_responses = []  # Store intercepted API responses here

def handle_response(response):
    """
    This function is called automatically every time
    the browser receives a response from any URL.
    We filter for JSON responses only.
    """
    content_type = response.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            data = response.json()
            captured_responses.append({
                "url": response.url,
                "status": response.status,
                "data": data
            })
            print(f"Intercepted JSON from: {response.url}")
        except:
            pass  # Some responses claim JSON but fail to parse — skip them


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    # ── ATTACH THE LISTENER BEFORE NAVIGATING ──
    # This is critical — attach before goto() so you capture
    # every response including the very first ones that load
    page.on("response", handle_response)

    print("Navigating to page — intercepting all network responses...\n")
    page.goto("https://quotes.toscrape.com/api/quotes?page=1")
    page.wait_for_load_state("networkidle")  # Wait until all network activity settles

    browser.close()

# ── REVIEW WHAT WAS CAPTURED ─────────────
print(f"\nTotal JSON responses captured: {len(captured_responses)}")

for i, item in enumerate(captured_responses):
    print(f"\n--- Response {i+1} ---")
    print(f"URL: {item['url']}")
    print(f"Status: {item['status']}")
    print(f"Data preview: {str(item['data'])[:300]}...")

# Save captured data
with open("intercepted_data.json", "w", encoding="utf-8") as f:
    json.dump(captured_responses, f, indent=2, ensure_ascii=False)

print("\nSaved to intercepted_data.json")