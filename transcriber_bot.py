#!/usr/bin/env python

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
    print("TRANSCRIBE BOT")
    print("by /u/isaac_lo\n")
    print("------------------------\n")
    post_log = PostLog(PATH)

    config = Config(PATH)

    # checks if this is the first time the config has been created
    if config.firstrun:
        # if so, the bot will stop
        print("\nFirst run. A default config has been created.")
        print("Please edit this config before further use of the transcribe" +
              " bot")
        print("Bot Stopped!")
        print("\n------------------------\n")
        return

    # otherwise, start the bot
    print("\nBot Started!")
    print("\n------------------------\n")
    bot = Bot(post_log, config)
    bot.run()

if __name__ == "__main__":
    # run main method
    main()
