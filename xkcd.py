import os
from random import randint
from urllib.parse import urlparse

import requests


def get_random_comic_num():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    total_comics = int(response.json()["num"])
    random_comics_num = randint(0, total_comics)
    return random_comics_num


def save_comic(num):
    random_comics_url = f"https://xkcd.com/{num}/info.0.json"
    response = requests.get(random_comics_url)
    response.raise_for_status()

    comic_url_for_download = response.json()["img"]
    comic_name = response.json()["title"]
    comic_comment = response.json()["alt"]
    parsed_url = urlparse(comic_url_for_download)
    comic_extension = os.path.splitext(parsed_url.path)[1]
    comic_filename = f"{comic_name}{comic_extension}"

    download_response = requests.get(comic_url_for_download)
    download_response.raise_for_status()

    with open(comic_filename, "wb") as file:
        file.write(download_response.content)
    return comic_filename, comic_comment
