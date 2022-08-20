import requests


def get_url_for_upload(group_id, token):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {"access_token": token, "v": "5.131", "group_id": group_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_comic_to_server(filename, url_for_upload):
    with open(filename, "rb") as file:
        files = {"photo": file}
        response = requests.post(url_for_upload, files=files)
    response.raise_for_status()
    upload_response = response.json()
    photo_server = upload_response["server"]
    photo = upload_response["photo"]
    photo_hash = upload_response["hash"]
    return photo_server, photo, photo_hash


def upload_comic_in_album(photo_server, photo, photo_hash, token):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "v": "5.131",
        "access_token": token,
        "group_id": "215364307",
        "server": photo_server,
        "photo": photo,
        "hash": photo_hash,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    upload_response = response.json()
    upload_owner_id = upload_response['response'][0]['owner_id']
    photo_id = upload_response["response"][0]["id"]
    return upload_owner_id, photo_id


def publish_comic(upload_owner_id, photo_id, token, group_id, comment):
    url = "https://api.vk.com/method/wall.post"
    group_id = f"-{group_id}"
    attachments = f"photo{upload_owner_id}_{photo_id}"
    params = {
        "v": "5.131",
        "access_token": token,
        "owner_id": group_id,
        "from_group": 1,
        "message": comment,
        "attachments": attachments,
    }
    publish_response = requests.post(url, params=params)
    publish_response.raise_for_status()
    return publish_response
