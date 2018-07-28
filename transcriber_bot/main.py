"""Main run file for the reddit transcriber bot"""

from multiprocessing import Process
from transcriber_bot.config import Config
import praw

def main():
    """Main method for reddit transcriber bot"""
    reddit = praw.Reddit(client_id=Config.CLIENT_ID,
                         client_secret=Config.CLIENT_SECRET,
                         user_agent=Config.USER_AGENT,
                         username=Config.USERNAME,
                         password=Config.PASSWORD)

    jobs = []

    # comment_watcher
    jobs.append(Process(name="Comments:",
                        target=comment_watcher))

    # start threads
    for job in jobs:
        job.start()

if __name__ == "__main__":
    main()
