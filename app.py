from config import *

from db import DB
from api import PodcastIndexAPI

import os, configparser

class App:
    def __init__(self) -> None:
        self.load_config()
        self.api: PodcastIndexAPI = PodcastIndexAPI(PODCASTINDEX_KEY, PODCASTINDEX_SECRET)
        self.db: DB = DB("./data/test.sqlite")

    ################################################ CONFIG ################################################
    
    def load_config(self) -> None:
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        if not os.path.isfile("./config.ini"):
            with open("./config.ini", "w") as file:
                file.close()
        self.config.read("./config.ini")

    def get_config_as_json(self) -> dict:
        d: dict = {}
        for key in self.config["config"]:
            d[key] = self.config["config"][key]
        return d

    def set_config(self, data: dict) -> None:
        for key in data:
            if self.config["config"][key] != data[key]: self.config["config"][key] = data[key]
        self.write_config()

    def write_config(self) -> None:
        with open("./config.ini", "w") as file:
            self.config.write(file)
            file.close()

    ########################################################################################################

    ############################################### ACTIONS ################################################

    def update_episodes(self) -> None:
        feeds = self.db.get_properties_from_table("id", "podcasts")

        for feed in feeds:
            feed_id = feed[0]
            eps = self.api.get_episodes_by_id(str(feed_id))
            
            if eps is not None and len(eps["items"]) > 0:
                self.db.add_episodes(eps["items"])

    # def download_episodes(self) -> None:
    #     pass

    # def verify_ep_files(self) -> None:
    #     pass

    # def download_episode(self, ep_link: str, location: str) -> None:
    #     pass

    def add_podcast_to_subscriptions(self, pod_id: str) -> None:
        podcast = self.api.get_feed_by_id(pod_id)
        if podcast is not None:
            self.db.add_podcast(podcast["feed"])
            self.update_episodes()

    ########################################################################################################

    ################################################# API ##################################################

    def get_episodes_by_podcast(self, podcast_id: int) -> list:
        return self.db.get_episodes_by_podcast(podcast_id)
    
    def get_podcasts_by_name(self, title: str) -> list:
        data = self.api.get_podcast_by_title(title)
        if data is not None and len(data["feeds"]) > 0: return data["feeds"]
        return []
    
    def get_all_podcasts(self) -> list:
        return self.db.get_podcasts()
    
    def get_podcast_info(self, podcast_id: int) -> dict:
        data = {
            "podcast": self.db.get_podcasts_by_id(podcast_id),
            "episodes": self.get_episodes_by_podcast(podcast_id)
        }
        return data
    
    def get_image(self, podcast_id: int) -> str:
        exists = os.path.isfile(f"static/covers/{podcast_id}--artwork.jpg")
        if not exists:
            filename = self.db.cache_image(str(podcast_id), "", True)
            if filename: return filename
            return "default.jpg"
        else:
            return f"{podcast_id}--artwork.jpg"

    ########################################################################################################

if __name__ == "__main__":
    app = App()
    # app.get_episodes_by_podcast(359782)
    print(app.get_config_as_json())