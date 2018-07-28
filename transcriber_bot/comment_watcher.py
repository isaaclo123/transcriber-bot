#!/usr/bin/env python3

"""Contains comment watcher code"""

import config
import praw

COMMENT_COMMAND = "Transcribe!"

def main():
    """Watches reddit comments"""
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         user_agent=config.USER_AGENT,
                         username=config.USERNAME,
                         password=config.PASSWORD)

    subreddit_list = config.SUBREDDIT_LIST

    # if no subreddits to watch, end comment_watcher
    if not subreddit_list:
        return

    # otherwise create subreddits stream string
    subreddit_stream = subreddit_list[0]
    for i in range(1, len(subreddit_list)):
        subreddit_stream += "+{subreddit}".format(subreddit=subreddit_list[i])

    subreddits = reddit.subreddit(subreddit_stream).stream

    # loop through comment stream
    for submission in subreddits.submissions():
        print(submission.url)
        # if submission.body == COMMENT_COMMAND:
        # TODO: add item with comment object. look at comment.submission's
        # image and reply to comment object
        # queue.push()
        # pass

if __name__ == '__main__':
    main()
