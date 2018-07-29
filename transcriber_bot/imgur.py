"""Helper methods for managing imgur links"""

import json
import requests

def get_imgur_url(imgur_image):
    """returns imgur image link from imgur image object

    :imgur_image: imgur image object
        {
            'hash':'xZEPnZu',
            'title':'Short bio example',
            'description':None,
            'has_sound':False,
            'width':791,
            'height':1024,
            'size':206030,
            'ext':'.jpg',
            'animated':False,
            'prefer_video':False,
            'looping':False,
            'datetime':'2015-02-12 13:58:18'
        }
    :returns: valid link to imgur image, or None, if invalid

    """
    imgur_hash = imgur_image.get('hash')
    imgur_ext = imgur_image.get('ext')

    # checks if the imgur image object has a 'hash' and 'ext' within it
    if imgur_hash and imgur_ext:
        return 'https://imgur.com/{hash}{ext}'.format(hash=imgur_hash,
                                                       ext=imgur_ext)

    # otherwise return None if canot create imgur object
    return None


def get_imgur_urls(imgur_url):
    """Searches for imgur images

    :imgur_url: imgur url
    :returns: list of imgur image urls

    """

    # convert i.imgur.com/xZEPnZu to i.imgur.com/xZEPnZu.json
    imgur_json = requests.get('{url}.json'.format(url=imgur_url)).text
    imgur_data = json.loads(imgur_json)

    print(imgur_data)

    images = None

    try:
        images = imgur_data['data']['image']['album_images']['images']
    except KeyError:
        # if images is invalid, print out statement and return empty list
        print('Invalid imgur data')
        return []

    image_urls = []

    for image in images:
        image_link = get_imgur_url(image)
        # if an image link can be created
        if image_link:
            # add it to image_urls
            image_urls.append(image_link)

    return image_urls

print(get_imgur_urls("https://imgur.com/gallery/2OMsd"))
