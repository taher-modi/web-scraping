import requests
import json

# ─────────────────────────────────────────
# Reddit exposes JSON data by appending .json to any page URL
# We found this by watching the Network tab in DevTools
# ─────────────────────────────────────────

url = "https://www.reddit.com/r/python/.json"

# Reddit blocks the default Python user-agent — we need custom headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

params = {
    "limit": 10  # Get top 10 posts
}

response = requests.get(url, headers=headers, params=params)
print(f"Status: {response.status_code}")

data = response.json()

# Navigate the JSON structure to find the posts
posts = data["data"]["children"]

print(f"\nFound {len(posts)} posts\n")
print("=== TOP POSTS IN r/python ===")

all_posts = []

for post in posts:
    post_data = post["data"]  # Actual post data is nested under "data"

    title = post_data["title"]
    author = post_data["author"]
    score = post_data["score"]
    comments = post_data["num_comments"]
    url_link = post_data["url"]

    print(f"\nTitle: {title}")
    print(f"Author: u/{author}")
    print(f"Score: {score} | Comments: {comments}")
    print(f"Link: {url_link}")

    all_posts.append({
        "title": title,
        "author": author,
        "score": score,
        "comments": comments,
        "url": url_link
    })

# Save to JSON
with open("reddit_posts.json", "w", encoding="utf-8") as f:
    json.dump(all_posts, f, indent=2, ensure_ascii=False)

print("\nSaved to reddit_posts.json")