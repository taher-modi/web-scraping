"""
TOOL SELECTION DECISION GUIDE
Use this as a reference when starting any new scraping task.

─────────────────────────────────────────────────────────
USE requests + BeautifulSoup WHEN:
─────────────────────────────────────────────────────────
  ✓ The data is visible in page source (Ctrl+U in browser)
  ✓ The site is static HTML with no JavaScript rendering
  ✓ You need maximum speed across thousands of pages
  ✓ Example: Wikipedia, static news sites, government data portals

─────────────────────────────────────────────────────────
USE requests directly (API approach) WHEN:
─────────────────────────────────────────────────────────
  ✓ You can see a JSON API call in DevTools Network tab
  ✓ The site loads data via background XHR/Fetch calls
  ✓ You want the fastest and most stable scraping approach
  ✓ Example: Reddit, Twitter, most modern SPAs

─────────────────────────────────────────────────────────
USE Playwright WHEN:
─────────────────────────────────────────────────────────
  ✓ The page is JavaScript-rendered (empty source)
  ✓ You want to intercept API responses via network listener
  ✓ You need fast browser automation with minimal boilerplate
  ✓ You are starting a new project and have free choice of tool
  ✓ Example: React/Vue apps, sites with heavy JS rendering

─────────────────────────────────────────────────────────
USE Selenium WHEN:
─────────────────────────────────────────────────────────
  ✓ The existing codebase already uses Selenium
  ✓ The target site specifically blocks Playwright's fingerprint
  ✓ You need broader browser support (Firefox, Edge, Safari)
  ✓ Example: Legacy enterprise projects, cross-browser testing

─────────────────────────────────────────────────────────
DECISION FLOW FOR ANY NEW TASK:
─────────────────────────────────────────────────────────
  1. Open the site → press Ctrl+U → is your data in the source?
     YES → use requests + BeautifulSoup
     NO  → go to step 2

  2. Open DevTools → Network tab → Fetch/XHR filter → reload page
     → Can you see a JSON API call returning your data?
     YES → call that API directly with requests
     NO  → go to step 3

  3. The site needs a real browser.
     → Use Playwright (preferred) or Selenium
     → Consider network interception before HTML parsing
"""

print("Decision guide loaded. Refer to this file when starting new tasks.")