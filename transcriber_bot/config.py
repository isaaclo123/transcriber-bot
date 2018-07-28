"""Configuration values for the reddit transcriber bot"""

import os

class Config(object):
    """Configuration class for reddit transcriber bot"""

    # reddit client id
    CLIENT_ID = os.environ.get('CLIENT_ID')

    # reddit client secret
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    # reddit client password
    PASSWORD = os.environ.get('PASSWORD')

    # reddit client user agent text
    USER_AGENT = 'transcriber-bot'

    # reddit client username
    USERNAME = os.environ.get('USERNAME')

    # list of subreddits to watch
    SUBREDDIT_LIST = [
        '4chan',
    ]
