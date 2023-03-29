from config import *

from db import DB
from api import PodcastIndexAPI

class App:
    def __init__(self) -> None:
        self.api = PodcastIndexAPI(PODCASTINDEX_KEY, PODCASTINDEX_SECRET)
        self.db = DB("./data/test.sqlite")

    def update_episodes(self) -> None:
        feeds = self.db.get_properties_from_table("id", "podcasts")

        for feed in feeds:
            feed_id = feed[0]
            eps = self.api.get_episodes_by_id(str(feed_id))
            
            if eps is not None and len(eps["items"]) > 0:
                self.db.add_episodes(eps["items"])
    
    def fetch_episodes(self, pod_id: int) -> dict | None: # @temp
        return self.api.get_episodes_by_id(str(pod_id))

    def download_episodes(self) -> None:
        pass

    def verify_ep_files(self) -> None:
        pass

    def download_episode(self, ep_link: str, location: str) -> None:
        pass

    def add_podcast_to_subscriptions(self, pod_id: str) -> None:
        podcast = self.api.get_feed_by_id(pod_id)
        if podcast is not None:
            self.db.add_podcast(podcast["feed"])

    # API
    def get_episodes_by_podcast(self, podcast_id: int) -> list:
        return self.db.get_episodes_by_podcast(podcast_id)
    
    def get_podcasts_by_name(self, title: str) -> list:
        data = self.api.get_podcast_by_title(title)
        if data is not None and len(data["feeds"]) > 0: return data["feeds"]
        return []
    
    def get_all_podcasts(self) -> list:
        return self.db.get_podcasts()

if __name__ == "__main__":
    app = App()
    app.get_episodes_by_podcast(359782)