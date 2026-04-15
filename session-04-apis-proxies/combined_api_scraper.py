import requests
import json
import random
import time

# ─────────────────────────────────────────
# A production-style API scraper using:
# - requests.Session for efficiency
# - Custom headers with rotation
# - Proxy-ready configuration
# - Pagination through an API
# ─────────────────────────────────────────

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36"
]

# ── SET UP SESSION ───────────────────────
session = requests.Session()
session.headers.update({
    "User-Agent": random.choice(USER_AGENTS),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5"
})

# Proxy config — ready to plug in when Tendem provides credentials
# session.proxies = {
#     "http": "http://username:password@proxy-host:port",
#     "https": "http://username:password@proxy-host:port"
# }


# ── PAGINATE THROUGH GITHUB API ──────────
all_repos = []
pages_to_fetch = 3  # 3 pages x 10 results = 30 repos

print("Fetching Python scraping repos from GitHub API...\n")

for page in range(1, pages_to_fetch + 1):
    params = {
        "q": "scraping python",
        "sort": "stars",
        "per_page": 10,
        "page": page
    }

    response = session.get("https://api.github.com/search/repositories", params=params)

    if response.status_code != 200:
        print(f"Page {page} failed with status {response.status_code}")
        continue

    data = response.json()
    repos = data["items"]

    for repo in repos:
        all_repos.append({
            "name": repo["name"],
            "owner": repo["owner"]["login"],
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "description": repo["description"],
            "url": repo["html_url"]
        })

    print(f"Page {page}: fetched {len(repos)} repos")
    time.sleep(1)  # Respect the API rate limit

print(f"\nTotal repos collected: {len(all_repos)}")

# ── EXPORT ───────────────────────────────
with open("github_repos.json", "w", encoding="utf-8") as f:
    json.dump(all_repos, f, indent=2, ensure_ascii=False)

print("Saved to github_repos.json")
print("\n✅ Done.")