# Podcast Aggregator Py

A flask app to find and download podcasts

## Installation

1. Clone this repo
2. Install dependencies - `pip install flask requests pathvalidate`
3. Create a file called `config.ini` in the project root directory
4. Also create a file called `config.py`
5. Run the app - `python server.py`
6. Open `http://localhost:5000` in your browser

### `config.ini`

```ini
[config]
DOWNLOAD_DIR = D:/Path_where_to_store_downloaded_podcasts
```
### `config.py`

1. Create an account on [PodcastIndex](https://api.podcastindex.org/)
2. Put your API_KEY and SECRET in this file as follows
```py
PODCASTINDEX_KEY = "YOUR-API-KEY"
PODCASTINDEX_SECRET = "YOUR-SECRET"
```

The app may have bugs, and if you find any, feel free to open an issue or PR(after opening the issue)
