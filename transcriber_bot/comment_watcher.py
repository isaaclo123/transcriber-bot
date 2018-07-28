"""Contains comment watcher code"""

from transcriber_bot.config import Config
import praw

COMMENT_COMMAND = "Transcribe!"

queue = []

def main():
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
        subreddit_stream += "+{subreddit}".format(subreddit=subreddit_list[i])

    comments = reddit.subreddit(subreddit_stream).stream.comments()

    # loop through comment stream
    for comment in comments:
        if comment.body == COMMENT_COMMAND:
            # TODO: add item with comment object. look at comment.submission's
            # image and reply to comment object
            # queue.push()
            pass

if __name__ == '__main__':
    main()
