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
        return response.json()


def upload_comic_in_album(response, token):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "v": "5.131",
        "access_token": token,
        "group_id": "215364307",
        "server": response["server"],
        "photo": response["photo"],
        "hash": response["hash"],
    }
    upload_response = requests.post(url, params=params)
    upload_response.raise_for_status()
    return upload_response.json()


def publish_comic(response, token, group_id, comment):
    url = "https://api.vk.com/method/wall.post"
    owner_id = "-" + group_id
    photo_id = response["response"][0]["id"]
    attachments = (
        "photo"
        + str(response["response"][0]["owner_id"])
        + "_"
        + str(photo_id)
    )
    params = {
        "v": "5.131",
        "access_token": token,
        "owner_id": owner_id,
        "from_group": 1,
        "message": comment,
        "attachments": attachments,
    }
    publish_response = requests.post(url, params=params)
    publish_response.raise_for_status()
    return publish_response
