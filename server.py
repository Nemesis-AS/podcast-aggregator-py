from flask import Flask, render_template, request, jsonify
# from utils import file_to_dict

from app import App

class Server:
    def __init__(self, name, app: App) -> None:
        self.name = name
        self.app = app
        self.create_app()

    def create_app(self) -> None:
        self.server = Flask(__name__)

        @self.server.route("/")
        def view_index_page() -> str:
            return render_template("index.html")
        
        @self.server.route("/add/new")
        def view_add_pod_page() -> str:
            return render_template("addpodcast.html")

        @self.server.route("/settings")
        def view_settings_page() -> str:
            return render_template("settings.html")

        @self.server.route("/viewfeed/<int:feed_id>")
        def view_feeg_page(feed_id: int) -> str:
            return render_template("viewfeed.html", feed_id=feed_id)



        @self.server.route("/config", methods=["GET", "POST"])
        def config(): # @todo
            # print(request.method == "POST")
            match request.method:
                case "GET":
                    config = self.app.get_config_as_json()
                    return jsonify(config)
                case "POST":
                    body = request.json
                    if body: 
                        self.app.set_config(body)
                        return ("", 200)
                    return ("", 400)
            return ("", 404)


        @self.server.route("/feeds", methods=["GET"])
        def feeds():
            match request.method:
                case "GET":
                    data = self.app.get_all_podcasts()
                    return jsonify({ "feeds": data })
            return ""
        
        @self.server.route("/get-podcast-episodes/<int:podcast_id>", methods=["GET"])
        def get_eps_by_podcast(podcast_id: int):
            return jsonify(self.app.get_episodes_by_podcast(podcast_id))
        
        @self.server.route("/get-podcast-info/<int:podcast_id>", methods=["GET"])
        def get_podcast_info(podcast_id: int):
            return jsonify(self.app.get_podcast_info(podcast_id))

        @self.server.route("/get-podcast-by-name", methods=["GET"])
        def fetch_podcast():
            query = request.args.get("query")
            if query is not None:
                return jsonify(self.app.get_podcasts_by_name(query))
            return jsonify([])
        
        @self.server.route("/add-podcast", methods=["GET"])
        def add_podcast():
            pod_id = request.args.get("pod_id")
            if pod_id is not None:
                self.app.add_podcast_to_subscriptions(pod_id)
            return jsonify({"status": pod_id is not None})
        
        @self.server.route("/podcast/delete/<int:podcast_id>", methods=["GET"])
        def podcast_delete(podcast_id: int):
            self.app.db.remove_podcast(podcast_id)
            return ("", 200)
        
        @self.server.route("/episode/delete/<int:episode_id>", methods=["GET"])
        def episode_delete(episode_id: int):
            self.app.db.remove_episode(episode_id)
            return ("", 200)

        @self.server.route("/podcast/artwork/<int:podcast_id>")
        def podcast_artwork(podcast_id: int):
            cache = self.app.get_image(podcast_id)
            if cache:
                return cache
            else:
                return ""


    def start(self) -> None:
        self.server.run(debug=True)

if __name__ == "__main__":
    app = Server(__name__, App())
    app.start()