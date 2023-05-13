from config import *

from db import DB
from api import PodcastIndexAPI

import requests
from configparser import ConfigParser
from os.path import isfile, normpath, join
from pathlib import Path
from pathvalidate import sanitize_filename
from subprocess import Popen
import concurrent.futures


class App:
    def __init__(self) -> None:
        self.load_config()
        self.api: PodcastIndexAPI = PodcastIndexAPI(
            PODCASTINDEX_KEY, PODCASTINDEX_SECRET
        )
        self.db: DB = DB("./data/test.sqlite")
        self.scheduler = concurrent.futures.ThreadPoolExecutor(
            max_workers=2, thread_name_prefix="scheduler"
        )

    ################################################ CONFIG ################################################

    def load_config(self) -> None:
        self.config: ConfigParser = ConfigParser()
        if not isfile("./config.ini"):
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
            if self.config["config"][key] != data[key]:
                self.config["config"][key] = data[key]
        self.write_config()

    def write_config(self) -> None:
        with open("./config.ini", "w") as file:
            self.config.write(file)
            file.close()

    ########################################################################################################

    ############################################## SCHEDULING ##############################################

    def schedule_task(self, task: str, args: list) -> bool:
        match task:
            case "download_ep":
                self.scheduler.submit(self.download_episode, args[0])
            case "download_pod":
                self.scheduler.submit(self.download_podcast, args[0])
        return True

    ########################################################################################################

    ############################################### ACTIONS ################################################

    def update_episodes(self) -> None:
        feeds = self.db.get_properties_from_table("id", "podcasts")

        for feed in feeds:
            feed_id = feed[0]
            eps = self.api.get_episodes_by_id(str(feed_id))

            if eps is not None and len(eps["items"]) > 0:
                self.db.add_episodes(eps["items"])

    def download_podcast(self, podcast_id: str | int) -> bool:
        eps = self.db.get_episodes_by_podcast(podcast_id)
        output = True
        for ep in eps:
            res = self.download_episode(ep[0])
            if not res:
                output = res
        return output

    def download_episode(self, ep_id: str | int) -> bool:
        # print("Downloading")
        root_dir = self.config.get("config", "download_dir")
        ep_info = self.db.get_episode_by_id(ep_id)
        pod_title = sanitize_filename(self.db.get_podcasts_by_id(ep_info[10])[1])
        ep_title = sanitize_filename(ep_info[1], "_", "auto")
        dir = normpath(join(root_dir, pod_title))
        location = normpath(join(dir, f"{ep_title}.mp3"))
        Path(dir).mkdir(parents=True, exist_ok=True)

        download_url = ep_info[13]
        if not download_url:
            return False

        res = requests.get(download_url, stream=True)
        chunk_size = 2048

        # clen_header = res.headers.get("Content-Length")
        # total_size = int(clen_header) if clen_header else 0

        # curr_chunk = 0
        res.raise_for_status()
        with open(location, "wb") as file:
            for chunk in res.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                # curr_chunk += 1
                # percentage = ((curr_chunk * chunk_size) / total_size) * 100
        self.db.episode_mark_downloaded(ep_id)
        return True

    # def debug_download(self, ep_id: str | int) -> bool:
    #     print("Debug Downloading", ep_id)
    #     sleep(1)
    #     return True

    # def debug_download_pod(self, podcast_id: str | int) -> bool:
    #     eps = self.db.get_episodes_by_podcast(podcast_id)
    #     output = True
    #     for ep in eps:
    #         res = self.debug_download(ep[0])
    #         if not res:
    #             output = res
    #     return output

    def add_podcast_to_subscriptions(self, pod_id: str) -> None:
        podcast = self.api.get_feed_by_id(pod_id)
        if podcast is not None:
            self.db.add_podcast(podcast["feed"])
            self.update_episodes()

    ########################################################################################################

    ################################################## FS ##################################################

    def verify_podcast(self, podcast_id: str | int) -> None:
        episodes = self.db.get_episodes_by_podcast(podcast_id)
        for ep in episodes:
            self.verify_episode(ep[0])

    def verify_episode(self, episode_id: str | int) -> None:
        root_dir = self.config.get("config", "download_dir")

        ep_info = self.db.get_episode_by_id(episode_id)
        pod_title = self.db.get_podcasts_by_id(ep_info[10])[1]

        ep_title = sanitize_filename(ep_info[1], "_", "auto")
        dir = join(root_dir, pod_title)
        location = join(dir, f"{ep_title}.mp3")

        if isfile(location):
            self.db.episode_mark_downloaded(episode_id)
        else:
            self.db.episode_mark_downloaded(episode_id, True)

    def open_podcast_dir(self, podcast_id: str | int) -> None:
        root_dir = self.config.get("config", "download_dir")
        pod_info = self.db.get_podcasts_by_id(podcast_id)
        dir = normpath(join(root_dir, pod_info[1]))
        Popen(f"explorer {dir}")  # @temp Works on WINDOWS only

    ########################################################################################################

    ################################################# API ##################################################

    def get_episodes_by_podcast(self, podcast_id: int) -> list:
        return self.db.get_episodes_by_podcast(podcast_id)

    def get_podcasts_by_name(self, title: str) -> list:
        data = self.api.get_podcast_by_title(title)
        if data is not None and len(data["feeds"]) > 0:
            return data["feeds"]
        return []

    def get_all_podcasts(self) -> list:
        return self.db.get_podcasts()

    def get_podcast_info(self, podcast_id: int) -> dict:
        data = {
            "podcast": self.db.get_podcasts_by_id(podcast_id),
            "episodes": self.get_episodes_by_podcast(podcast_id),
        }
        return data

    def get_image(self, podcast_id: int) -> str:
        exists = isfile(f"static/covers/{podcast_id}--artwork.jpg")
        if not exists:
            filename = self.db.cache_image(str(podcast_id), "", True)
            if filename:
                return filename
            return "default.jpg"
        else:
            return f"{podcast_id}--artwork.jpg"

    ########################################################################################################


if __name__ == "__main__":
    app = App()
