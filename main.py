import os

from dotenv import load_dotenv

from vk_api import (
    get_url_for_upload,
    publish_comic,
    upload_comic_in_album,
    upload_comic_to_server,
)
from xkcd import get_total_comics, save_comic


if __name__ == "__main__":
    load_dotenv()
    group_id = os.getenv("VK_GROUP_ID")
    token = os.getenv("VK_ACCESS_TOKEN")

    total_comics = get_total_comics()
    comic_filename, comic_comment = save_comic(total_comics)

    try:
        url_for_upload = get_url_for_upload(group_id, token)
        photo_server, photo, photo_hash = upload_comic_to_server(
            comic_filename,
            url_for_upload,
        )
        upload_owner_id, photo_id = upload_comic_in_album(
            photo_server,
            photo,
            photo_hash,
            token,
            group_id,
        )
        publish_comic(upload_owner_id, photo_id, token, group_id, comic_comment)
    finally:
        os.remove(comic_filename)
