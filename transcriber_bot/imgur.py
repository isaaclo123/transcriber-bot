"""Helper methods for managing imgur links"""

from bs4 import BeautifulSoup
import requests

def get_imgur_urls(imgur_url):
    """Searches for imgur images

    :imgur_url: imgur url
    :returns: list of imgur image urls
    """

    imgur_page = requests.get(imgur_url)
    soup = BeautifulSoup(imgur_page, 'html.parser')
    images = soup.find_all('.post-image-placeholder img')
    image_urls = []

    for image in images:
        # add image src attribute contents to image_urls
        image_src = image.get('src')
        # because src attributes are in form "//i.imgur.com/xZEPnZu.jpg", add
        # "https:" to front
        src_url = "https:{src}".format(src=image_src)

        image_urls.append(src_url)

    return image_urls
