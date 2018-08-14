"""Contains PRAW reddit bot test code"""

import os
from transcriber_bot.config import Config
from transcriber_bot.models import PostLog
from transcriber_bot.bot import Bot, BOT_FOOTER, BOT_HEADER

# path above test directory (working directory)
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def test_init_valid_config():
    """tests Bot initialization valid

    assumes valid config in root directory

    """

    post_log = PostLog(PATH)
    config = Config(PATH)

    bot = Bot(post_log, config)
    # set debug to true
    bot.debug = True
    # assert bot initialized flag
    assert bot.initialized

    # assert bot run to completion
    assert bot.run()

def test_format_reddit_text_fail():
    """test reddit bot formatting failure"""
    # null
    assert not Bot.format_reddit_text(None)
    # empty
    assert not Bot.format_reddit_text("")
    # length too small
    assert not Bot.format_reddit_text("h")
    # text is all spaces
    assert not Bot.format_reddit_text("     ")

def test_format_reddit_text_valid():
    """test reddit bot text formatting is correct"""
    before = "\n\n\n\r\n\n    test1\n\ntest2\ntest\n      \n"
    after = "> test1\n>\n> test2 test\n\n"

    assert Bot.format_reddit_text(before) == after

def test_get_reddit_message_text_fail():
    """test reddit bot message text failure"""

    assert not Bot.get_reddit_message_text(None, None)
    assert not Bot.get_reddit_message_text(["testurl1.com"], None)
    assert not Bot.get_reddit_message_text([], "testposturl.com")
    assert not Bot.get_reddit_message_text(None, "testposturl.com")

def test_get_reddit_message_text_valid():
    """test reddit bot message text handling is correct"""

    # from test_album "https://imgur.com/a/NyHaeak"
    img_urls = ["https://i.imgur.com/IXM9pIo.jpg",
                "https://i.imgur.com/K1SXVRF.jpg",
                "https://i.imgur.com/q6tL7p3.jpg"]

    message = Bot.get_reddit_message_text(img_urls, "testposturl.net",
                                          max_length=100)

    print(message)

    # assert message is not too long but still exists
    assert 100 < len(message) < (len(BOT_FOOTER) + len(BOT_HEADER) +
                                 (2 * len("testposturl.net")) + 120)

    # assert correct bot header
    assert message.startswith(BOT_HEADER)
    # assert correct bot footer
    assert message.endswith(BOT_FOOTER)
