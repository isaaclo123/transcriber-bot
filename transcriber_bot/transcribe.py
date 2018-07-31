#!/usr/bin/env python3

"""Contains comment watcher code"""

from imgur import is_url_imgur, get_imgur_urls
from reddit import is_url_reddit, get_reddit_urls
import config
import praw

def main():
    """Watches reddit comments"""
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         user_agent=config.USER_AGENT,
                         username=config.USERNAME,
                         password=config.PASSWORD)

    subreddit_list = config.SUBREDDIT_LIST

    # if no subreddits to watch, end program
    if not subreddit_list:
        return

    # otherwise create subreddits stream string
    subreddit_stream = subreddit_list[0]
    for i in range(1, len(subreddit_list)):
        subreddit_stream += "+{subreddit}".format(subreddit=subreddit_list[i])

    subreddits = reddit.subreddit(subreddit_stream).stream

    # loop through submissions in subreddit stream
    for submission in subreddits.submissions():
        url = submission.url
        print("url: {url}".format(url=url))
        img_urls = []

        if is_url_imgur(url):
            # if url is imgur
            img_urls = get_imgur_urls(url)
        elif is_url_reddit(url):
            # if url is reddit
            img_urls = get_reddit_urls(url)
        else:
            # url invalid
            print("url invalid, skipping")
            img_urls = []

        if img_urls:
            # if urls is not empty
            # TODO: do something with img_urls
            pass

if __name__ == '__main__':
    main()
