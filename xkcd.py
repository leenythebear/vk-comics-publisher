import os
from random import randint
from urllib.parse import urlparse

import requests


def get_total_comics():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    total_comics = int(response.json()["num"])
    return total_comics


def save_comic(total_comics):
    random_comics_num = randint(0, total_comics)
    random_comics_url = f"https://xkcd.com/{random_comics_num}/info.0.json"
    response = requests.get(random_comics_url)
    response.raise_for_status()

    comic_response = response.json()
    download_url = comic_response["img"]
    comic_name = comic_response["title"]
    comic_comment = comic_response["alt"]
    parsed_url = urlparse(download_url)
    comic_extension = os.path.splitext(parsed_url.path)[1]
    comic_filename = f"{comic_name}{comic_extension}"

    download_response = requests.get(download_url)
    download_response.raise_for_status()

    with open(comic_filename, "wb") as file:
        file.write(download_response.content)
    return comic_filename, comic_comment
