import os
from urllib.parse import urlparse

import requests


def get_comics_extension(url):
    parsed_link = urlparse(url)
    return os.path.splitext(parsed_link.path)[1]


def get_comics_filename(extension, filename):
    comics_filename = f'{filename}{extension}'
    return comics_filename


def get_random_comics(num):
    comics_url = f"https://xkcd.com/{num}/info.0.json"
    response = requests.get(comics_url)
    response.raise_for_status()
    return response.json()


def save_comics(url, comics_filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(f"{comics_filename}", "wb") as file:
        file.write(response.content)