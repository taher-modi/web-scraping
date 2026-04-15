import requests
import json

# ─────────────────────────────────────────
# PART 1: BASIC API CALL
# The GitHub API returns JSON directly — no HTML parsing needed
# ─────────────────────────────────────────

url = "https://api.github.com/search/repositories"

# APIs accept parameters via "params" — these get added to the URL automatically
params = {
    "q": "web scraping python",   # Search query
    "sort": "stars",              # Sort by most starred
    "per_page": 10                # Return 10 results
}

response = requests.get(url, params=params)

print(f"Status code: {response.status_code}")
print(f"Content type: {response.headers['Content-Type']}")

# .json() parses the response directly into a Python dictionary
data = response.json()

print(f"\nTotal results found: {data['total_count']}")
print(f"Results returned: {len(data['items'])}")

print("\n=== TOP 10 WEB SCRAPING REPOS ON GITHUB ===")
for repo in data["items"]:
    print(f"\nName: {repo['name']}")
    print(f"Owner: {repo['owner']['login']}")
    print(f"Stars: {repo['stargazers_count']}")
    print(f"Description: {repo['description']}")
    print(f"URL: {repo['html_url']}")