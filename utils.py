import json, requests

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