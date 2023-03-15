from app import App
from server import Server

def main() -> None:
    app = App()
    server = Server("pod_app", app)
    server.start()

main()