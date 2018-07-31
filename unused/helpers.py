"""General helper methods"""

import requests

MAX_TIMEOUT = 10 # 10 second timeout

IMAGE_EXTS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
]

def is_url_up(url):
    """check if a url is up

    :url: an url
    :returns: boolean that is true if valid

    """
    try:
        data = requests.get(url, timeout=MAX_TIMEOUT)
        # return true if statis code is not 404
        return data.status_code != 404
    except requests.Timeout:
        print("Request timed out")
        return False
    except requests.RequestException:
        print("Internet issue, requests error")
        return False
    except BaseException as error:
        print("Base exception: {error}".format(error=error))
        return False

def is_url_img(url):
    """check if a url is up

    :url: an url
    :returns: boolean that is true if valid

    """
    try:
        data = requests.get(url, timeout=MAX_TIMEOUT)
        # return true if statis code is not 404
        return data.status_code != 404
    except requests.Timeout:
        print("Request timed out")
        return False
    except requests.RequestException:
        print("Internet issue, requests error")
        return False
    except BaseException as error:
        print("Base exception: {error}".format(error=error))
        return False

def is_url_img(url, host):
    """check if a url is a valid image url

    :url: an url
    :host: a url host string
    :returns: true if url is imgur url

    """
    if not url.startswith(host):
        # if the url is not a {host} link, return an empty list
        return False

    for ext in IMAGE_EXTS:
        # loop through IMAGE_EXTS to find if the host url is a valid image
        if url.endswith(ext) and is_url_up(url):
            # if the url ends with a valid image extension and it it a valid url
            # resource, return a list with the url inside
            return True

    return False

def is_url_host(url):
    """check if a url is up

    :url: an url
    :returns: boolean that is true if valid

    """
    try:
        data = requests.get(url, timeout=MAX_TIMEOUT)
        # return true if statis code is not 404
        return data.status_code != 404
    except requests.Timeout:
        print("Request timed out")
        return False
    except requests.RequestException:
        print("Internet issue, requests error")
        return False
    except BaseException as error:
        print("Base exception: {error}".format(error=error))
        return False
