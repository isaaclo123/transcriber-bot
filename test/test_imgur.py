"""Contains test code for imgur link handling"""

from transcriber_bot.imgur import is_url_imgur, get_imgur_data, get_imgur_urls

def test_is_url_imgur_fail():
    """ensure imgur url checking when fails"""
    assert not is_url_imgur(None)
    assert not is_url_imgur("notimgur.com")
    # assert escaping
    assert not is_url_imgur("https:*'//i.imgur.com/notvaliditem.jpg/\\?=5'*")

def test_is_url_imgur_valid():
    """ensure imgur url checking when valid"""
    assert is_url_imgur("https://i.imgur.com/a/NyHaeak")

def test_get_imgur_data_fail():
    """test getting imgur json data from imgur url fail"""
    assert not get_imgur_data(None)
    assert not get_imgur_data("notimgur.com")
    assert not get_imgur_data("https://i.imgur.com/notvaliditem.jpg")
    # assert escaping
    assert not get_imgur_data("https://i.imgur.com/notvaliditem.jpg/\\?=5'*")

def test_get_imgur_data_valid():
    """test getting imgur json data from imgur url when valid input"""
    imgur_data = get_imgur_data("https://imgur.com/gallery/2OMsd")
    imgur_image = imgur_data["data"]["image"]["album_images"]["images"][0]
    print(imgur_image)
    assert imgur_data
    assert imgur_image["hash"] == "xZEPnZu"
    assert imgur_image["ext"] == ".jpg"

def test_get_imgur_urls_fail():
    """test imgur image link from imgur image object when fail"""
    assert not get_imgur_urls(None)
    assert not get_imgur_urls("notimgur.com")
    assert not get_imgur_urls("https://i.imgur.com/a/notvaliditem")
    # assert escaping
    assert not get_imgur_urls("https://i.imgur.com/notvaliditem/\\?=5'*")

def test_get_imgur_urls():
    """test imgur image link from imgur image object valid input"""
    imgur_album = get_imgur_urls("https://imgur.com/gallery/2OMsd")
    assert len(imgur_album) == 4
