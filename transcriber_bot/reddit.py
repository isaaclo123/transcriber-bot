"""Helper methods for managing reddit links"""

import requests
from requests.utils import quote

MAX_TIMEOUT = 10 # 10 second timeout
REDDIT_URL = "https://i.redd.it/"
QUOTE_CHARS = "/:"

IMAGE_EXTS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
]

def is_url_reddit(reddit_url):
    """check if a url is a reddit url

    :reddit_url: reddit url
    :returns: boolean that is true if url is reddit url

    """
    if reddit_url:
        reddit_url = quote(reddit_url, safe=QUOTE_CHARS)
    else:
        return False
    return reddit_url.startswith(REDDIT_URL)

def check_reddit_data(reddit_url):
    """check if reddit url is valid resource

    :reddit_url: reddit url
    :returns: boolean that is true if valid

    """
    try:
        if reddit_url:
            reddit_url = quote(reddit_url, safe=QUOTE_CHARS)
        else:
            return False
        reddit_data = requests.get(reddit_url, timeout=MAX_TIMEOUT)
        # return true if statis code is not 404
        return reddit_data.status_code != 404
    except requests.Timeout:
        print("Request timed out")
        return False
    except requests.RequestException:
        print("Internet issue, requests error")
        return False
    except BaseException as error:
        print("Base exception: {error}".format(error=error))
        return False

def get_reddit_urls(reddit_url):
    """checks if a url is a reddit media link and returns a list with the url/s

    :reddit_url: reddit media url
    :returns: list with reddit image, or empty list, if invalid

    """

    if reddit_url:
        reddit_url = quote(reddit_url, safe=QUOTE_CHARS)
    else:
        return []

    if not is_url_reddit(reddit_url):
        # if the url is not a reddit link, return an empty list
        return []

    for ext in IMAGE_EXTS:
        # loop through IMAGE_EXTS to find if the reddit url is a valid image
        if reddit_url.endswith(ext) and check_reddit_data(reddit_url):
            # if the url ends with a valid image extension and it it a valid url
            # resource, return a list with the reddit_url inside
            return [reddit_url]

    return []
