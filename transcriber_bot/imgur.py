"""Helper methods for managing imgur links"""

import json
import requests

MAX_TIMEOUT = 10 # 10 second timeout
MAX_IMAGE_COUNT = 4 # only 4 album images max allowed to be parsed by bot
IMGUR_URL = "https://imgur.com/"

def is_url_imgur(imgur_url):
    """check if a url is an imgur url

    :imgur_url: reddit url
    :returns: boolean that is true if url is imgur url

    """
    return imgur_url.startswith(IMGUR_URL)

def get_imgur_data(imgur_url):
    """get imgur json data from imgur url

    :imgur_url: imgur url
    :returns: imgur data in python form

    """
    try:
        # convert i.imgur.com/xZEPnZu to i.imgur.com/xZEPnZu.json
        imgur_json = requests.get("{url}.json".format(url=imgur_url),
                                  timeout=MAX_TIMEOUT).text
        imgur_data = json.loads(imgur_json)
        return imgur_data
    except requests.Timeout:
        print("Request timed out on {}".format(imgur_url))
        return None
    except requests.RequestException:
        print("Internet issue, requests error on {}".format(imgur_url))
        return None
    except json.decoder.JSONDecodeError:
        # if images is invalid, print out statement and return None
        print("Invalid JSON data on {}".format(imgur_url))
        return None
    except BaseException as error:
        print("Base exception: {}".format(error))
        return None

def get_imgur_url(imgur_image):
    """returns imgur image link from imgur image object

    :imgur_image: imgur image object
        {
            "hash":"xZEPnZu",
            "title":"Short bio example",
            "description":None,
            "has_sound":False,
            "width":791,
            "height":1024,
            "size":206030,
            "ext":".jpg",
            "animated":False,
            "prefer_video":False,
            "looping":False,
            "datetime":"2015-02-12 13:58:18"
        }
    :returns: valid link to imgur image, or None, if invalid

    """
    imgur_hash = imgur_image.get("hash")
    imgur_ext = imgur_image.get("ext")

    # checks if the imgur image object has a "hash" and "ext" within it
    if imgur_hash and imgur_ext:
        return "{url}{hash}{ext}".format(url=IMGUR_URL,
                                         hash=imgur_hash,
                                         ext=imgur_ext)

    # otherwise return None if canot create imgur object
    return None

def get_imgur_urls(imgur_url):
    """Searches for imgur images

    :imgur_url: imgur url
    :returns: list of imgur image urls

    """

    # get imgur json data
    imgur_data = get_imgur_data(imgur_url)

    if not imgur_data:
        # if imgur data invalid, return empty list
        return []

    try:
        images = imgur_data["data"]["image"]["album_images"]["images"]
        image_urls = []

        image_count = 0
        for image in images:
            image_link = get_imgur_url(image)
            # if an image link can be created
            if image_link:
                # add it to image_urls
                image_urls.append(image_link)
                image_count += 1

                if image_count >= MAX_IMAGE_COUNT:
                    # break if album has too many images
                    break

        return image_urls

    except KeyError:
        # if images is invalid, print out statement and return empty list
        print("Invalid imgur data, KeyError")
        return []
    except ValueError:
        # if images is invalid, print out statement and return empty list
        print("Invalid imgur data, ValueError")
        return []
    except BaseException as error:
        print("Base exception: {error}".format(error=error))
        return []
