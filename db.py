import sqlite3
from time import time
import requests

class DB:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.build_db()
    
    def build_db(self) -> None:
        if not self.table_exists("podcasts"):
            self.cursor.execute("CREATE TABLE podcasts(id, title, link, desc, author, artwork, last_upload, itunes_id, lang, explicit, ep_count, categories, last_updated)")
        if not self.table_exists("episodes"):
            self.cursor.execute("CREATE TABLE episodes(id, title, link, desc, date_pub, duration, explicit, episode, season, artwork, podcast, downloaded, file_path, download_link)") # Download_URL
        if not self.table_exists("images"):
            self.cursor.execute("CREATE TABLE images(url, image)")

    def table_exists(self, table_name: str) -> bool:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE name = ?", [table_name]) 
        return bool(self.cursor.fetchone())

    def get_podcasts(self) -> list:
        return self.return_all("SELECT * FROM podcasts")

    def get_podcasts_by_id(self, pod_id: str | int) -> list:
        self.cursor.execute("SELECT * FROM podcasts WHERE id = ?", [int(pod_id)])
        return self.cursor.fetchone()

    def get_episodes_by_podcast(self, podcast: str | int) -> list:
        self.cursor.execute("SELECT * FROM episodes WHERE podcast = ? ORDER BY date_pub DESC", [int(podcast)])
        return self.cursor.fetchall()
    
    def get_episode_by_id(self, ep_id: str | int) -> list:
        self.cursor.execute("SELECT * FROM episodes WHERE id = ?", [int(ep_id)])
        return self.cursor.fetchone()

    def add_podcast(self, podcast: dict) -> None: # Add Podcast Class
        if self.item_exists("podcasts", "id", podcast["id"]): return

        self.cursor.execute("INSERT INTO podcasts VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            podcast["id"],
            podcast["title"],
            podcast["link"],
            podcast["description"],
            podcast["author"],
            podcast["artwork"],
            podcast["lastUpdateTime"],
            podcast["itunesId"],
            podcast["language"],
            podcast["explicit"],
            podcast["episodeCount"],
            str(podcast["categories"]),
            time()
        ])

        self.cache_image(podcast["id"], podcast["artwork"])
        self.conn.commit()

    def add_episodes(self, episodes: list[dict]) -> None: # Add Episode Class        
        for episode in episodes:
            if self.item_exists("episodes", "id", episode["id"]): continue

            self.cursor.execute("INSERT INTO episodes VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            episode["id"],
            episode["title"],
            episode["link"],
            episode["description"],
            episode["datePublished"],
            episode["duration"],
            episode["explicit"],
            episode["episode"],
            episode["season"],
            episode["image"],
            episode["feedId"],
            False,
            "",
            episode["enclosureUrl"]
        ])
        self.conn.commit()
    
    def remove_podcast(self, pod_id: str | int) -> None:
        self.remove_episodes_by_podcast(pod_id)

        if not self.item_exists("podcasts", "id", int(pod_id)): return
        self.cursor.execute("DELETE FROM podcasts WHERE id = ?", [int(pod_id)])
        self.conn.commit()

    def remove_episode(self, ep_id: str | int) -> None:
        if not self.item_exists("episodes", "id", int(ep_id)): return
        self.cursor.execute("DELETE FROM episodes WHERE id = ?", [int(ep_id)])
        self.conn.commit()

    def remove_episodes_by_podcast(self, pod_id: str | int) -> None:
        self.cursor.execute("DELETE FROM episodes WHERE podcast = ?", [int(pod_id)])
        self.conn.commit()

    def episode_mark_downloaded(self, ep_id: str | int, unmark: bool = False) -> None:
        value = "0" if unmark else "1"
        self.cursor.execute(f"UPDATE episodes SET downloaded = {value} WHERE id = ?", [int(ep_id)])
        self.conn.commit()

    def cache_image(self, pod_id: str | int, url: str = "", return_name: bool = False) -> None | str:
        if not url: 
            self.cursor.execute("SELECT artwork FROM podcasts WHERE id = ?", [int(pod_id)])
            url = self.cursor.fetchone()[0]

        if not url: return None

        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            with open(f"static/covers/{pod_id}--artwork.jpg", "wb") as img:
                for chunk in req.iter_content(chunk_size=128):
                    img.write(chunk)
            if return_name: return "{pod_id}--artwork.jpg"

    def close(self) -> None:
        self.conn.close()
    
    def return_all(self, statement: str) -> list:
        self.cursor.execute(statement)
        return self.cursor.fetchall()
    
    def item_exists(self, table: str, property: str, value: str | int) -> bool:
        self.cursor.execute(f"SELECT {property} FROM {table} WHERE {property} = ?", [value]) 
        return bool(self.cursor.fetchone())
    
    def get_properties_from_table(self, property: str, table: str) -> list:
        self.cursor.execute(f"SELECT {property} FROM {table}")
        return self.cursor.fetchall()

# For Debugging
# if __name__ == "__main__":
#     db = DB("./data/dbtest.sqlite")
