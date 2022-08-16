from random import randint

import requests


def get_random_comics_num():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    total_comics = int(response.json()['num'])
    random_comics_num = randint(0, total_comics)
    return random_comics_num


