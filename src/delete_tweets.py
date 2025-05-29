from core.log import log
from core.memory import load_deleted_ids, save_deleted_ids
from core.twitter_api import get_user_id, fetch_latest_tweets, delete_tweet

def delete_from_api():
    deleted_ids = load_deleted_ids()
    user_id = get_user_id()
    if not user_id:
        return

    tweets = fetch_latest_tweets(user_id)
    if not tweets:
        log("✅ No tweets found.")
        return

    deleted = 0
    for tweet in tweets:
        if deleted >= 17:
            break
        if tweet["id"] in deleted_ids:
            continue
        if delete_tweet(tweet["id"], tweet["created_at"]):
            deleted_ids.add(tweet["id"])
            deleted += 1

    save_deleted_ids(deleted_ids)
    log(f"🏁 Deleted {deleted} tweet(s) from API.")

if __name__ == "__main__":
    delete_from_api()