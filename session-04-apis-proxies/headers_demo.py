import requests

# ─────────────────────────────────────────
# PART 1: SEE YOUR DEFAULT HEADERS
# httpbin.org is a free service that reflects your request back to you
# ─────────────────────────────────────────

response = requests.get("https://httpbin.org/headers")
print("=== DEFAULT HEADERS PYTHON SENDS ===")
print(response.json())

# You will see "User-Agent": "python-requests/2.x.x"
# Websites can see this and identify you as a bot


# ─────────────────────────────────────────
# PART 2: SEND CUSTOM HEADERS TO LOOK LIKE A BROWSER
# ─────────────────────────────────────────

custom_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

response = requests.get("https://httpbin.org/headers", headers=custom_headers)
print("\n=== CUSTOM HEADERS (LOOKS LIKE A REAL BROWSER) ===")
print(response.json())


# ─────────────────────────────────────────
# PART 3: USER-AGENT ROTATION
# For large scraping jobs, rotating between multiple User-Agents
# makes your traffic look less uniform and harder to detect
# ─────────────────────────────────────────
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

def get_random_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

# Simulate 5 requests with rotating headers
print("\n=== ROTATING USER-AGENTS ACROSS 5 REQUESTS ===")
for i in range(5):
    headers = get_random_headers()
    print(f"Request {i+1} User-Agent: {headers['User-Agent'][:60]}...")