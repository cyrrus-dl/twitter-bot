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
FETCHED_TWEETS_FILE = "fetched_tweets.json"
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

    def get_user_id(self) -> Optional[str]:
        """Get the authenticated user's ID."""
        self.log("🔍 Recherche de l'ID utilisateur...", Colors.CYAN)
        try:
            response = self._make_request("GET", "users/me")
            user_id = response["data"]["id"]
            self.log(f"✅ Authentification réussie pour l'utilisateur {user_id}", Colors.GREEN)
            return user_id
        except Exception as e:
            self.log(f"❌ Échec de l'authentification: {str(e)}", Colors.RED)
            return None

    def fetch_user_tweets(
        self,
        user_id: str,
        max_results: int = 100,
        fields: List[str] = ["created_at"]
    ) -> List[Dict[str, Any]]:
        """Fetch tweets for a specific user."""
        self.log("📥 Récupération des tweets...", Colors.CYAN)
        try:
            params = {
                "max_results": max_results,
                "tweet.fields": ",".join(fields)
            }
            response = self._make_request(
                "GET",
                f"users/{user_id}/tweets",
                params=params
            )
            return response.get("data", [])
        except Exception as e:
            self.log(f"❌ Échec de la récupération des tweets: {str(e)}", Colors.RED)
            return []

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

    def _load_fetched_tweets(self) -> List[Dict]:
        """Load fetched tweets from file."""
        if os.path.exists(FETCHED_TWEETS_FILE):
            with open(FETCHED_TWEETS_FILE, 'r') as f:
                tweets = json.load(f)
                self.log(f"📖 {len(tweets)} tweets chargés depuis le cache", Colors.BLUE)
                return tweets
        return []

    def _save_fetched_tweets(self, tweets: List[Dict]) -> None:
        """Save fetched tweets to file."""
        with open(FETCHED_TWEETS_FILE, 'w') as f:
            json.dump(tweets, f)
        self.log(f"💾 {len(tweets)} tweets mis en cache", Colors.BLUE)

    def _remove_fetched_tweet(self, tweet_id: str) -> None:
        """Remove a tweet from the fetched tweets cache."""
        tweets = self._load_fetched_tweets()
        original_count = len(tweets)
        tweets = [t for t in tweets if t["id"] != tweet_id]
        self._save_fetched_tweets(tweets)
        self.log(f"🗑️ Tweet {tweet_id} retiré du cache ({original_count} → {len(tweets)})", Colors.YELLOW)

    def fetch_latest_tweets(self, user_id: str) -> List[Dict]:
        """Fetch the latest tweets for the user."""
        tweets = self.fetch_user_tweets(user_id)
        if tweets:
            oldest = min(tweets, key=lambda t: t["created_at"])
            newest = max(tweets, key=lambda t: t["created_at"])
            self.log(f"📊 {len(tweets)} tweets récupérés ({oldest['created_at']} à {newest['created_at']})", Colors.GREEN)
        else:
            self.log("ℹ️ Aucun tweet trouvé", Colors.YELLOW)

        self._save_fetched_tweets(tweets)
        return sorted(tweets, key=lambda t: t["created_at"])

    def delete_oldest_tweets(self) -> None:
        """Main method to delete oldest tweets."""
        self.log("🚀 Démarrage du processus de suppression...", Colors.MAGENTA)

        # Load previously deleted tweets
        deleted_ids = self._load_deleted_ids()
        self.log(f"📊 {len(deleted_ids)} tweets précédemment supprimés trouvés", Colors.BLUE)

        # Get user ID
        user_id = self.get_user_id()
        if not user_id:
            self.log("❌ Impossible de continuer sans ID utilisateur", Colors.RED)
            return

        # Fetch and process tweets
        tweets = self.fetch_latest_tweets(user_id)
        if not tweets:
            self.log("ℹ️ Aucun tweet à traiter", Colors.YELLOW)
            return

        # Process tweets
        deleted = 0
        skipped = 0
        for tweet in tweets:
            if deleted >= MAX_DELETIONS:
                self.log(f"⏹️ Limite de suppression atteinte ({MAX_DELETIONS})", Colors.YELLOW)
                break

            tweet_id = tweet["id"]
            if tweet_id in deleted_ids:
                self.log(f"⏭️ Tweet {tweet_id} déjà supprimé, passage au suivant", Colors.YELLOW)
                skipped += 1
                continue

            if self.delete_tweet(tweet_id):
                deleted_ids.add(tweet_id)
                deleted += 1
                self._remove_fetched_tweet(tweet_id)
                self.log("⏳ Attente d'une seconde avant la prochaine suppression...", Colors.CYAN)
                time.sleep(1)  # Rate limiting

        # Save results
        self._save_deleted_ids(deleted_ids)
        self.log(f"🏁 Processus terminé: {deleted} nouveaux tweets supprimés, {skipped} ignorés", Colors.GREEN)
        self.log(f"📊 Total des tweets supprimés: {len(deleted_ids)}", Colors.BLUE)

def main():
    try:
        deleter = TwitterDeleter()
        deleter.delete_oldest_tweets()
    except Exception as e:
        TwitterDeleter.log(f"❌ Une erreur est survenue: {str(e)}", Colors.RED)

if __name__ == "__main__":
    main()