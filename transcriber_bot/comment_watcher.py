"""Contains comment watcher code"""

from transcriber_bot.config import Config
import praw

def comment_watcher():
    """Watches reddit comments"""
    reddit = praw.Reddit(client_id=Config.CLIENT_ID,
                         client_secret=Config.CLIENT_SECRET,
                         user_agent=Config.USER_AGENT,
                         username=Config.USERNAME,
                         password=Config.PASSWORD)

    subreddit_list = Config.SUBREDDIT_LIST

    # if no subreddits to watch, end comment_watcher
    if not subreddit_list:
        return

    # otherwise create subreddits stream string
    subreddit_stream = subreddit_list[0]
    for i in range(1, len(subreddit_list)):
        subreddit_stream += "+{subreddit}".format(subreddit_list[i])

    stream = praw.helpers.comment_stream(r, subreddit_stream, limit=None)

    for comment in reddit.subreddit(Config.SUBREDDIT_LIST).stream.comments():
        print(comment)
