import requests
import time
from core.auth import auth
from core.log import log

MAX_DELETIONS = 17

def get_user_id():
    log("🔍 Getting user ID...")
    r = requests.get("https://api.twitter.com/2/users/me", auth=auth)
    if r.status_code != 200:
        log(f"❌ Failed to get user ID: {r.text}")
        return None
    return r.json()["data"]["id"]

def fetch_latest_tweets(user_id):
    log("📥 Fetching up to 100 latest tweets...")
    url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=100&tweet.fields=created_at"
    r = requests.get(url, auth=auth)
    if r.status_code == 429:
        log("⏳ Rate limit hit.")
        return []
    if r.status_code != 200:
        log(f"❌ Failed to fetch tweets: {r.text}")
        return []
    return sorted(r.json().get("data", []), key=lambda t: t["created_at"])

def delete_tweet(tweet_id, created_at=None):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    r = requests.delete(url, auth=auth)
    if r.status_code == 200:
        log(f"🗑️ Deleted tweet ID {tweet_id}" + (f" from {created_at}" if created_at else ""))
        return True
    else:
        log(f"⚠️ Failed to delete tweet {tweet_id}. Status: {r.status_code}")
        return False