import os
import json

DELETED_FILE = "deleted_tweets.json"

def load_deleted_ids():
    if os.path.exists(DELETED_FILE):
        with open(DELETED_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_deleted_ids(ids):
    with open(DELETED_FILE, 'w') as f:
        json.dump(list(ids), f)