from config import *
from hashlib import sha1
import json, time, requests

class PodcastIndexAPI:
    def __init__(self, key: str, secret: str) -> None:
        self.API_KEY = key
        self.API_SECRET = secret
        self.BASE_URL = "https://api.podcastindex.org/api/1.0/"


    def get_podcast_by_title(self, title: str) -> None:
        res: dict = self.request_builder("/search/bytitle", {
            "q": title
        })
        if not res["status"]:
            print(f"Couldn't find {title}")
            return
        for idx in range(len(res["feeds"])):
            print(f"{idx + 1}. {res['feeds'][idx]['title']}")
        

    def get_episodes_by_id(self, feed_id: str) -> dict | None:
        res: dict = self.request_builder("/episodes/byfeedid", {
            "id": feed_id
        })

        if not res["status"]:
            print(f"Couldn't find {feed_id}")
            return
        return res
        # for idx in range(len(res["items"])):
            # print(f"{idx + 1}. {res['items'][idx]['title']}")
            # print(f"{idx + 1}. {res['items'][idx]['enclosureUrl']}")


    def request_builder(self, endpoint: str, query: dict) -> dict:
        epoch = str(int(time.time()))
        auth = sha1((self.API_KEY + self.API_SECRET + epoch).encode("utf-8")).hexdigest()
        headers = {
            "X-Auth-Key": self.API_KEY,
            "X-Auth-Date": epoch,
            "Authorization": auth
        }
        res: requests.Response = requests.get(self.BASE_URL + endpoint, params=query, headers=headers)
        try:
            json = res.json()
            return json
        except:
            print("Received Invalid Response!")
            return {}
# Utils
def dict_to_file(data: dict, file_path: str) -> None:
    with open(file_path, "w") as file:
        json.dump(data, file)

def file_to_dict(file_path: str) -> dict | list:
    with open(file_path, "r") as file:
        return json.load(file)

def download_episode(url: str) -> None:
    res = requests.get(url)
    ep = res.content
    with open("data/ep.mp3", "wb") as file:
        file.write(ep)

def main() -> None:
    api = PodcastIndexAPI(PODCASTINDEX_KEY, PODCASTINDEX_SECRET)
    feeds = {}

    subs = file_to_dict("data/subscriptions.json")
    for sub in subs:
        feed = api.get_episodes_by_id(sub)
        if feed: feeds[sub] = feed

    with open("data/feeds.json", "w") as file:
        json.dump(feeds, file)
    
    print("Written Feeds Successfully!")

main()