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
        
        @self.server.route("/add/new")
        def add_pod() -> str:
            return render_template("addpodcast.html")

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
                    data = self.app.get_all_podcasts()
                    return jsonify({ "feeds": data })
                    # feed = file_to_dict("data/feeds.json")
                    # return jsonify(feed)
            return ""
        
        @self.server.route("/get-podcast-episodes/<int:podcast_id>", methods=["GET"])
        def get_eps_by_podcast(podcast_id: int):
            return jsonify(self.app.get_episodes_by_podcast(podcast_id))
        
        @self.server.route("/get-podcast-by-name", methods=["GET"])
        def fetch_podcast():
            query = request.args.get("query")
            if query is not None:
                return jsonify(self.app.get_podcasts_by_name(query))
            return jsonify([])
        
        # @self.server.route("/test", methods=["GET"])
        # def test_route():
        #     pod_id = request.args.get("podid")
        #     if not pod_id: return jsonify({})
        #     return jsonify(self.app.fetch_episodes(int(pod_id)))
        
        @self.server.route("/add-podcast", methods=["GET"])
        def add_podcast():
            pod_id = request.args.get("pod_id")
            if pod_id is not None:
                self.app.add_podcast_to_subscriptions(pod_id)
            return jsonify({"status": pod_id is not None})

    def start(self) -> None:
        self.server.run(debug=True)

if __name__ == "__main__":
    app = Server(__name__, App())
    app.start()