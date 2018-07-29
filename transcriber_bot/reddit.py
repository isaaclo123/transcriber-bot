"""Helper methods for managing reddit links"""

import requests

MAX_TIMEOUT = 10 # 10 second timeout
REDDIT_URL = "https://i.redd.it/"

IMAGE_EXTS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
]

def check_reddit_data(reddit_url):
    """check if reddit url is valid resource

    :reddit_url: imgur url
    :returns: boolean that is true if valid

    """
    try:
        reddit_data = requests.get(reddit_url, timeout=MAX_TIMEOUT)
        # return true if statis code is not 404
        return reddit_data.status_code != 404
    except requests.Timeout:
        print("Request timed out")
    except requests.RequestException:
        print("Internet issue, requests error")
    except BaseException as error:
        print("Base exception: {error}".format(error=error))

    return False

def get_reddit_urls(reddit_url):
    """checks if a url is a reddit media link and returns a list with the url/s

    :reddit_url: reddit media url
    :returns: list with reddit image, or empty list, if invalid

    """

    if not reddit_url.startswith(REDDIT_URL):
        # if the url is not a reddit link, return an empty list
        return []

    for ext in IMAGE_EXTS:
        # loop through IMAGE_EXTS to find if the reddit url is a valid image
        if reddit_url.endswith(ext) and check_reddit_data(reddit_url):
            # if the url ends with a valid image extension and it it a valid url
            # resource, return a list with the reddit_url inside
            return [reddit_url]

    return []
