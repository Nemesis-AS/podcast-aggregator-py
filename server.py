from flask import Flask, render_template, request, jsonify
from utils import file_to_dict

from app import App

class Server:
    def __init__(self, name, app: App) -> None:
        self.name = name
        self.app = app
        self.create_app()

    def create_app(self) -> None:
        self.server = Flask(__name__)

        @self.server.route("/")
        def index() -> str:
            return render_template("index.html")
        
        @self.server.route("/viewfeed/<int:feed_id>")
        def viewfeed(feed_id: int) -> str:
            return render_template("viewfeed.html", feed_id=feed_id)

        @self.server.route("/config", methods=["GET", "POST"])
        def config() -> str: # @todo
            match request.method:
                case "GET":
                    pass
                case "POST":
                    pass
            return ""

        @self.server.route("/feeds", methods=["GET"])
        def feeds(): # @todo
            match request.method:
                case "GET":
                    feed = file_to_dict("data/feeds.json")
                    return jsonify(feed)
            return ""
        
        @self.server.route("/get-podcast-episodes/<int:podcast_id>", methods=["GET"])
        def get_eps_by_podcast(podcast_id: int):
            return jsonify(self.app.get_episodes_by_podcast(podcast_id))
            return jsonify({"res": "Echo: " + str(podcast_id)})

    def start(self) -> None:
        self.server.run(debug=True)

if __name__ == "__main__":
    app = Server(__name__, App())
    app.start()