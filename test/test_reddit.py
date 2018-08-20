"""Helper methods for managing reddit links"""

from transcriber_bot.reddit import (
    is_url_reddit,
    check_reddit_data,
    get_reddit_urls
)

VALID_REDDIT_URL = "https://i.redd.it/j6es640k1qe11.jpg"

def test_is_url_reddit_fail():
    """ensure reddit url checking when fails"""
    assert not is_url_reddit(None)
    assert not is_url_reddit("notreddit.com")
    # assert escaping
    assert not is_url_reddit("https:*'//i.reddit.com/notvaliditem.jpg/\\?=5'*")

def test_is_url_reddit_valid():
    """ensure reddit url checking when valid"""
    assert is_url_reddit(VALID_REDDIT_URL)

def test_check_reddit_data_fail():
    """test getting reddit data from reddit url fail"""
    assert not check_reddit_data(None)
    assert not check_reddit_data("notreddit.com")
    print("test check reddit data fail")
    print(check_reddit_data("https://i.reddit.com/notvaliditem.jpg"))
    assert not check_reddit_data("https://i.reddit.com/notvaliditem.jpg")
    # assert escaping
    assert not check_reddit_data("https://i.reddit.com/notvaliditem.jpg/\\?='*")

def test_check_reddit_data_valid():
    """test getting reddit json data from reddit url"""
    assert check_reddit_data(VALID_REDDIT_URL)

def test_get_reddit_urls_fail():
    """test getting reddit urls fail"""
    assert not get_reddit_urls(None)
    assert not get_reddit_urls("notreddit.com")
    assert not get_reddit_urls("https://i.reddit.com/a/notvaliditem")
    # assert escaping
    assert not get_reddit_urls("https://i.reddit.com/notvaliditem/\\?=5'*")

def test_get_reddit_urls_valid():
    """test getting reddit urls from reddit url"""
    reddit_data = get_reddit_urls(VALID_REDDIT_URL)
    print(reddit_data)
    assert reddit_data
    assert reddit_data == [VALID_REDDIT_URL]
