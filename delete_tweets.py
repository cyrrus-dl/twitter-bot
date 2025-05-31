import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Set, Optional, Any
from abc import ABC, abstractmethod

# Constants
MAX_DELETIONS = 17
DELETED_FILE = "deleted_tweets.json"
TWEETS_FILE = "tweets.js"
API_BASE_URL = "https://api.twitter.com/2"

# ANSI Color Codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

class BaseTwitterAPI(ABC):
    def __init__(self):
        self._load_environment()
        self.auth = OAuth1(
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_token_secret
        )

    def _load_environment(self) -> None:
        """Load environment variables and validate them."""
        self.log("🔄 Chargement des variables d'environnement...", Colors.CYAN)
        load_dotenv()

        self.api_key = os.getenv('API_KEY')
        self.api_secret = os.getenv('API_SECRET')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("❌ Variables d'environnement manquantes")

    @staticmethod
    def log(message: str, color: str = Colors.WHITE) -> None:
        """Log a message with timestamp and color."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Colors.GRAY}📅 [{timestamp}]{Colors.RESET} {color}{message}{Colors.RESET}")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a request to the Twitter API."""
        url = f"{API_BASE_URL}/{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                auth=self.auth,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Erreur API: {str(e)}", Colors.RED)
            raise

    def delete_tweet(self, tweet_id: str) -> bool:
        """Delete a specific tweet."""
        self.log(f"🗑️ Suppression du tweet {tweet_id}", Colors.YELLOW)
        try:
            self._make_request("DELETE", f"tweets/{tweet_id}")
            self.log(f"✅ Tweet {tweet_id} supprimé avec succès", Colors.GREEN)
            return True
        except Exception as e:
            self.log(f"❌ Échec de la suppression du tweet {tweet_id}: {str(e)}", Colors.RED)
            return False

class TwitterDeleter(BaseTwitterAPI):
    def __init__(self):
        super().__init__()
        self.log("🚀 Initialisation du suppresseur de tweets...", Colors.MAGENTA)

    def _load_deleted_ids(self) -> Set[str]:
        """Load previously deleted tweet IDs."""
        if os.path.exists(DELETED_FILE):
            with open(DELETED_FILE, 'r') as f:
                ids = set(json.load(f))
                self.log(f"📖 {len(ids)} tweets précédemment supprimés chargés", Colors.BLUE)
                return ids
        return set()

    def _save_deleted_ids(self, ids: Set[str]) -> None:
        """Save deleted tweet IDs to file."""
        with open(DELETED_FILE, 'w') as f:
            json.dump(list(ids), f)
        self.log(f"💾 {len(ids)} IDs de tweets supprimés sauvegardés", Colors.BLUE)

    def _load_tweets_from_file(self) -> List[Dict]:
        """Load tweets from the tweets.js file."""
        if not os.path.exists(TWEETS_FILE):
            self.log(f"❌ Fichier {TWEETS_FILE} non trouvé", Colors.RED)
            return []

        try:
            with open(TWEETS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                # Remove the JavaScript wrapper and parse as JSON
                json_str = content.replace('window.YTD.tweets.part0 = ', '')
                tweets = json.loads(json_str)
                self.log(f"📖 {len(tweets)} tweets chargés depuis {TWEETS_FILE}", Colors.BLUE)
                return tweets
        except Exception as e:
            self.log(f"❌ Erreur lors de la lecture du fichier {TWEETS_FILE}: {str(e)}", Colors.RED)
            return []

    def delete_tweets_from_file(self) -> None:
        """Main method to delete tweets from the file."""
        self.log("🚀 Démarrage du processus de suppression...", Colors.MAGENTA)

        # Load previously deleted tweets
        deleted_ids = self._load_deleted_ids()
        self.log(f"📊 {len(deleted_ids)} tweets précédemment supprimés trouvés", Colors.BLUE)

        # Load tweets from file
        tweets = self._load_tweets_from_file()
        if not tweets:
            self.log("ℹ️ Aucun tweet à traiter", Colors.YELLOW)
            return

        # Process tweets
        deleted = 0
        skipped = 0
        for tweet_data in tweets:
            if deleted >= MAX_DELETIONS:
                self.log(f"⏹️ Limite de suppression atteinte ({MAX_DELETIONS})", Colors.YELLOW)
                break

            tweet = tweet_data["tweet"]
            tweet_id = tweet["id_str"]

            if tweet_id in deleted_ids:
                self.log(f"⏭️ Tweet {tweet_id} déjà supprimé, passage au suivant", Colors.YELLOW)
                skipped += 1
                continue

            if self.delete_tweet(tweet_id):
                deleted_ids.add(tweet_id)
                deleted += 1
                self.log("⏳ Attente d'une seconde avant la prochaine suppression...", Colors.CYAN)
                time.sleep(1)  # Rate limiting

        # Save results
        self._save_deleted_ids(deleted_ids)
        self.log(f"🏁 Processus terminé: {deleted} nouveaux tweets supprimés, {skipped} ignorés", Colors.GREEN)
        self.log(f"📊 Total des tweets supprimés: {len(deleted_ids)}", Colors.BLUE)

def main():
    try:
        deleter = TwitterDeleter()
        deleter.delete_tweets_from_file()
    except Exception as e:
        TwitterDeleter.log(f"❌ Une erreur est survenue: {str(e)}", Colors.RED)

if __name__ == "__main__":
    main()