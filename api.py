from hashlib import sha1
import time, requests

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

    def get_feed_by_id(self, feed_id: str) -> dict | None:
        res: dict = self.request_builder("/podcasts/byfeedid", {
            "id": feed_id
        })

        if not res["status"]:
            print(f"Couldn't find {feed_id}")
            return None
        return res
        

    def get_episodes_by_id(self, feed_id: str, max: int = 100) -> dict | None:
        res: dict = self.request_builder("/episodes/byfeedid", {
            "id": feed_id,
            "max": max
        })

        if not res["status"]:
            print(f"Couldn't find {feed_id}")
            return None
        return res


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