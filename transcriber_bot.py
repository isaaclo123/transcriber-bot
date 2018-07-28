"""Main run file for the reddit transcriber bot"""

import praw
import os

def run():
    """Run method for reddit transcriber bot"""
    reddit = praw.Reddit(client_id='my client id',
                         client_secret='my client secret',
                         user_agent='my user agent',
                         username='my username',
                         password='my password')

if __name == "__main__":
    # run main method
    run()
