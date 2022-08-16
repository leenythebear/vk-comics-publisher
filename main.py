import os
from dotenv import load_dotenv

from xkcd import get_random_comic_num, get_random_comic

from helper import (
    get_comics_extension,
    get_comics_filename,
    save_comic,
    del_used_comic,
)

from vk_api import (
    get_url_for_upload,
    upload_comic_to_server,
    upload_comic_in_album,
    publish_comic,
)


if __name__ == "__main__":
    load_dotenv()
    group_id = os.getenv("GROUP_ID")
    token = os.getenv("ACCESS_TOKEN")

    random_comic_num = get_random_comic_num()
    random_comic = get_random_comic(random_comic_num)
    comic_url = random_comic["img"]
    comic_name = random_comic["title"]
    comic_comment = random_comic["alt"]
    comic_extension = get_comics_extension(comic_url)
    comic_filename = get_comics_filename(comic_extension, comic_name)
    save_comic(comic_url, comic_filename)

    url_for_upload = get_url_for_upload(group_id, token)
    upload_server_response = upload_comic_to_server(
        comic_filename, url_for_upload
    )
    upload_album_response = upload_comic_in_album(
        upload_server_response, token
    )
    publish_comic(upload_album_response, token, group_id, comic_comment)
    del_used_comic(comic_filename)
