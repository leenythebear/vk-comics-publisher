import os
from dotenv import load_dotenv
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


def get_url_for_upload():
    group_id = '215364307'
    load_dotenv()
    token = os.getenv('ACCESS_TOKEN')
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': token, 'v': '5.131', "group_id": group_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_comics(filename, url_for_upload):
    with open(filename, 'rb') as file:
        files = {'photo': file}
        response = requests.post(url_for_upload, files=files)
        response.raise_for_status()
        return response.json()


def upload_comics_in_album(response):
    load_dotenv()
    token = os.getenv('ACCESS_TOKEN')
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {'v': '5.131', 'access_token': token, 'group_id': '215364307', 'server': response['server'], 'photo': response['photo'], 'hash': response['hash']}
    new_response = requests.post(url, params=params)
    new_response.raise_for_status()
    return new_response.json()


def publish_comics(response):
    load_dotenv()
    token = os.getenv('ACCESS_TOKEN')
    url = 'https://api.vk.com/method/wall.post'
    owner_id = '-' + '215364307'
    photo_id = response['response'][0]['id']
    attachments = 'photo' + str(response['response'][0]['owner_id']) + '_' + str(photo_id)
    params = {'v': '5.131', 'access_token': token,
              'owner_id': owner_id, 'from_group': 1, 'message': 'Comics',
              'attachments': attachments}
    publish_response = requests.post(url, params=params)
    publish_response.raise_for_status()
    return publish_response





if __name__ == "__main__":
    random_comics = get_random_comics(614)
    random_comics_url = random_comics['img']
    random_comics_comment = random_comics['alt']
    filename = random_comics['title']
    extension = get_comics_extension(random_comics_url)
    comics_filename = get_comics_filename(extension, filename)
    save_comics(random_comics_url, comics_filename)
