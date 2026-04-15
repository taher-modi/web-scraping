import requests

# ─────────────────────────────────────────
# PART 1: UNDERSTAND WHAT A PROXY DOES
# First check your real IP address
# ─────────────────────────────────────────

response = requests.get("https://httpbin.org/ip")
print(f"Your real IP: {response.json()['origin']}")


# ─────────────────────────────────────────
# PART 2: HOW TO CONFIGURE A PROXY IN REQUESTS
# This is the exact syntax used when Tendem provides you a proxy
# Format: "protocol://username:password@host:port"
# ─────────────────────────────────────────

# When Tendem gives you a proxy, you configure it exactly like this:
proxies = {
    "http": "http://username:password@proxy-host:port",
    "https": "http://username:password@proxy-host:port"
}

# Then pass it to any request:
# response = requests.get(url, proxies=proxies)
# Every request through this session will route via that proxy IP


# ─────────────────────────────────────────
# PART 3: USE A FREE PUBLIC PROXY TO TEST THE CONCEPT
# Note: Free proxies are unreliable — only for learning the concept
# In the real job, Tendem provides a reliable paid proxy
# ─────────────────────────────────────────

# Test with no proxy to confirm your baseline IP
response = requests.get("https://httpbin.org/ip")
print(f"\nWithout proxy - IP seen by server: {response.json()['origin']}")

print("\nProxy configuration syntax understood.")
print("When Tendem provides proxy credentials, plug them into the proxies dict above.")
print("The rest of your scraping code stays exactly the same — only the proxies dict changes.")


# ─────────────────────────────────────────
# PART 4: SESSION-LEVEL PROXY CONFIGURATION
# For real jobs, use a requests.Session() so every call uses the proxy
# without having to pass proxies= to every individual request
# ─────────────────────────────────────────

session = requests.Session()

# Set proxy once on the session
# session.proxies = proxies  # Uncomment when you have real proxy credentials

# Set headers once on the session — applies to every request automatically
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
})

# Now every call through this session uses the proxy and headers automatically
response = session.get("https://httpbin.org/headers")
print(f"\nSession headers confirmed: {response.json()['headers']['User-Agent'][:50]}...")

print("\n✅ Proxy configuration complete.")