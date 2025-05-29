import zipfile
import json
from core.log import log
from core.memory import load_deleted_ids, save_deleted_ids
from core.twitter_api import delete_tweet

ARCHIVE_ZIP = "tweet-archive.zip"
TARGET_FILE = "data/tweets.js"

def extract_tweet_ids_from_zip():
    if not zipfile.is_zipfile(ARCHIVE_ZIP):
        log("❌ Archive not found or invalid.")
        return []

    with zipfile.ZipFile(ARCHIVE_ZIP) as z:
        if TARGET_FILE not in z.namelist():
            log("❌ Archive missing expected file.")
            return []

        with z.open(TARGET_FILE) as f:
            content = f.read().decode("utf-8")
            content = content[content.find("["):]
            data = json.loads(content)
            return [t["id"] for t in data if "id" in t]

def delete_from_archive():
    deleted_ids = load_deleted_ids()
    tweet_ids = extract_tweet_ids_from_zip()
    to_delete = [tid for tid in tweet_ids if tid not in deleted_ids]

    deleted = 0
    for tweet_id in to_delete:
        if deleted >= 17:
            break
        if delete_tweet(tweet_id):
            deleted_ids.add(tweet_id)
            deleted += 1

    save_deleted_ids(deleted_ids)
    log(f"🏁 Deleted {deleted} tweet(s) from archive.")

if __name__ == "__main__":
    delete_from_archive()