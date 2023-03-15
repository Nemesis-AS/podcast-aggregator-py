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
    
    def download_episodes(self) -> None:
        pass

    def verify_ep_files(self) -> None:
        pass

    def download_episode(self, ep_link: str, location: str) -> None:
        pass

    # API
    def get_episodes_by_podcast(self, podcast_id: int) -> list:
        return self.db.get_episodes_by_podcast(podcast_id)

if __name__ == "__main__":
    app = App()
    app.get_episodes_by_podcast(359782)