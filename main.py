import os
from urllib.parse import urlparse


def get_comics_extension(url):
    parsed_link = urlparse(url)
    return os.path.splitext(parsed_link.path)[1]
