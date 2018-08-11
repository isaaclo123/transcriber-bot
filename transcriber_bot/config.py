"""Configuration values for the reddit transcriber bot"""

import os
import json
import configparser

def create_config():
    """Creates a ConfigParser config object for the transcriber bot

    :returns: ConfigParser config object

    """

    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'client_id': 'None',
        'client_secret': 'None',
        'user_agent': 'None',
        'username': 'None',
        'password': 'None',
        'subreddits': '[]'
    }

"""

# reddit client id
CLIENT_ID = 'bx2UN5dyZWVQuw' # os.environ.get('CLIENT_ID')

# reddit client secret
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

# reddit client password
PASSWORD = os.environ.get('PASSWORD')

# reddit client user agent text
USER_AGENT = 'transcriber-bot'

# reddit client username
USERNAME = 'isaac_lo' # os.environ.get('USERNAME')

# list of subreddits to watch
SUBREDDIT_LIST = [
    'testingground4bots',
]

class Config(object):
    # Config class for the reddit transcriber bot

    # reddit client id
    CLIENT_ID = 'bx2UN5dyZWVQuw' # os.environ.get('CLIENT_ID')

    # reddit client secret
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    # reddit client password
    PASSWORD = os.environ.get('PASSWORD')

    # reddit client user agent text
    USER_AGENT = 'transcriber-bot'

    # reddit client username
    USERNAME = 'isaac_lo' # os.environ.get('USERNAME')

    # list of subreddits to watch
    SUBREDDIT_LIST = [
        'testingground4bots',
    ]
"""
