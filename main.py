import os

from dotenv import load_dotenv

from vk_api import (
    get_url_for_upload,
    publish_comic,
    upload_comic_in_album,
    upload_comic_to_server,
)
from xkcd import get_random_comic_num, save_comic


if __name__ == "__main__":
    load_dotenv()
    group_id = os.getenv("VK_GROUP_ID")
    token = os.getenv("VK_ACCESS_TOKEN")

    random_comic_num = get_random_comic_num()
    comic_filename, comic_comment = save_comic(random_comic_num)

    try:
        url_for_upload = get_url_for_upload(group_id, token)
        upload_server_response = upload_comic_to_server(
            comic_filename, url_for_upload
        )
        upload_album_response = upload_comic_in_album(
            upload_server_response, token
        )
        publish_comic(upload_album_response, token, group_id, comic_comment)
    finally:
        os.remove(comic_filename)
