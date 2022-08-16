from random import randint

import requests


def get_random_comic_num():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    total_comics = int(response.json()['num'])
    random_comics_num = randint(0, total_comics)
    return random_comics_num


def get_random_comic(num):
    comics_url = f"https://xkcd.com/{num}/info.0.json"
    response = requests.get(comics_url)
    response.raise_for_status()
    return response.json()



