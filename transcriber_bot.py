#!/usr/bin/python3
"""Main run file for the reddit transcriber bot"""

import os
import praw
from transcriber_bot.config import Config
from transcriber_bot.models import PostLog
from transcriber_bot.bot import Bot

PATH = os.path.dirname(os.path.abspath(__file__))

def main():
    """main method for reddit transcriber bot"""
    # create an instance of the config
    print("Starting Transcribe Bot")
    print("---------------------------\n")
    post_log = PostLog(PATH)
    config = Config(PATH)
    bot = Bot(post_log, config)
    bot.run()

if __name__ == "__main__":
    # run main method
    main()
