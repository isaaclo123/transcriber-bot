"""Main run file for the reddit transcriber bot"""

from multiprocessing import Process
# from transcriber_bot.config import Config

def main():
    """Main method for reddit transcriber bot"""
    jobs = []

    # comment_watcher
    jobs.append(Process(name="Comments:",
                        target=comment_watcher))

    # start threads
    for job in jobs:
        job.start()

if __name__ == "__main__":
    main()
