import sqlite3

class DB:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.build_db()
    
    def build_db(self) -> None:
        if not self.table_exists("podcasts"):
            self.cursor.execute("CREATE TABLE podcasts(id, title, link, desc, author, artwork, last_upload, itunes_id, lang, explicit, ep_count, categories)")
        if not self.table_exists("episodes"):
            self.cursor.execute("CREATE TABLE episodes(id, title, link, desc, date_pub, duration, explicit, episode, season, artwork, podcast)") # downloaded, file_path
        if not self.table_exists("images"):
            self.cursor.execute("CREATE TABLE images(url, image)")

    def table_exists(self, table_name: str) -> bool:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE name = ?", [table_name]) 
        return bool(self.cursor.fetchone())

    def get_podcasts(self) -> list:
        return self.return_all("SELECT * FROM podcasts")

    def get_podcasts_by_property(self, property: str, value: str | int) -> list:
        self.cursor.execute("SELECT * FROM podcasts WHERE ? = ?", [property, str(value)])
        return self.cursor.fetchall()

    def get_episodes_by_podcast(self, podcast: str | int) -> list:
        self.cursor.execute("SELECT * FROM episodes WHERE podcast = ? ORDER BY date_pub DESC", [podcast])
        return self.cursor.fetchall()

    def add_podcast(self, podcast: dict) -> None: # Add Podcast Class
        if self.item_exists("podcasts", "id", podcast["id"]): return

        self.cursor.execute("INSERT INTO podcasts VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
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
            str(podcast["episodeCount"]),
        ])
        self.conn.commit()

    def add_episodes(self, episodes: list[dict]) -> None: # Add Episode Class        
        for episode in episodes:
            if self.item_exists("episodes", "id", episode["id"]): continue

            self.cursor.execute("INSERT INTO episodes VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
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
        ])
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
    
    def return_all(self, statement: str) -> list:
        self.cursor.execute(statement)
        return self.cursor.fetchall()
    
    def item_exists(self, table: str, property: str, value: str) -> bool:
        self.cursor.execute(f"SELECT {property} FROM {table} WHERE {property} = ?", [value]) 
        return bool(self.cursor.fetchone())
    
    def get_properties_from_table(self, property: str, table: str) -> list:
        self.cursor.execute(f"SELECT {property} FROM {table}")
        return self.cursor.fetchall()

# For Debugging
if __name__ == "__main__":
    db = DB("./data/dbtest.sqlite")

