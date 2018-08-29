"""Contains PRAW reddit bot code"""

import time
import praw
from transcriber_bot.imgur import is_url_imgur, get_imgur_urls
from transcriber_bot.reddit import is_url_reddit, get_reddit_urls
from transcriber_bot.ocr import get_image_text
from praw.exceptions import APIException, ClientException

BOT_HEADER = "A text transcription of"
BOT_FOOTER = ("Powered by [transcriber_bot]" +
              "(https://github.com/isaaclo123/transcriber_bot), /u/isaac_lo")
CONTINUED_MSG = "cont."
MAX_REPLY_LENGTH = 5000
DEBUG_MAX_RUNS = 2
API_PAUSE_TIME = 60
API_MAX_RETRIES = 2

class Bot(object):
    """Class for transcriber bot"""

    # set "initialized" marker to false
    initialized = False

    def __init__(self, post_log, config):
        """initializes Bot

        :post_log: a PostLog object
        :config: a ConfigParser config object

        """
        try:
            # debug var
            self.debug = config.debug

            self.reddit = praw.Reddit(client_id=config.client_id,
                                      client_secret=config.client_secret,
                                      user_agent=config.user_agent,
                                      username=config.username,
                                      password=config.password)

            subreddit_list = config.subreddits

            # if no subreddits to watch, don't run bot
            if not subreddit_list:
                print("no subreddits in list, Bot not initialized")
                return

            # set post log
            self.post_log = post_log

            # otherwise create subreddits stream string
            subreddit_stream = subreddit_list[0]
            for i in range(1, len(subreddit_list)):
                subreddit_stream += "+" + subreddit_list[i]

            self.subreddits = self.reddit.subreddit(subreddit_stream).stream

            # set variable indicating that the bot is initialized
            self.initialized = True
        except BaseException as error:
            print('Bot could not be initialized', error)
            return

    def run(self): #pylint: disable=too-many-branches
        """runs bot

        :returns: true when completed
        :raises: RuntimeException saying bot is not initialized

        """
        if not self.initialized or not self.subreddits:
            raise RuntimeError('Bot not initialized correctly')

        run_count = 0

        # loop through submissions in subreddit stream. If in debug, only
        # run DEBUG_MAX_RUNS times total
        for submission in self.subreddits.submissions():
            try:
                if self.debug:
                    print("run count for debug")
                    print(run_count)

                # if debug, increment run_count until DEBUG_MAX_RUNS and break
                if self.debug and run_count >= DEBUG_MAX_RUNS:
                    print("ending bot because DEBUG_MAX_RUNS reached")
                    break

                if self.post_log.is_in(submission.id):
                    # if the post id is already in the post log, skip processing
                    print("post {} has already been processed".format(
                        submission.id))
                    continue

                url = submission.url
                img_urls = []

                # increment run_count if in debug
                if self.debug:
                    run_count += 1

                if is_url_imgur(url):
                    # if url is imgur
                    img_urls = get_imgur_urls(url)
                elif is_url_reddit(url):
                    img_urls = get_reddit_urls(url)
                else:
                    # url invalid
                    img_urls = []
                    # decrease run_count if invalid
                    if self.debug:
                        run_count -= 1

                result_text = Bot.get_reddit_message_text(img_urls, url)
                # reply to submission
                self._reply_to_submission(submission, result_text)

            except APIException as error:
                # if api exception, retry posting API_MAX_RETRIES times
                print('Bot API error', error)

                time.sleep(API_PAUSE_TIME)

                # success flag for debug
                success = False

                for _ in range(API_MAX_RETRIES):
                    try:
                        self._reply_to_submission(submission, result_text)
                        # set success flag to true if works
                        success = True
                        break
                    except BaseException as error:
                        print('An error occoured: ', error)
                        time.sleep(API_PAUSE_TIME)

                if self.debug and not success:
                    # if the retries failed and debug is enabled, return false
                    return False

            except ClientException as error:
                print('Bot client error', error)
                # time.sleep(API_PAUSE_TIME)
                if self.debug:
                    return False
            except BaseException as error:
                print('Bot run error', error)
                # print error, return false if on debug
                if self.debug:
                    return False

        return True

    def _reply_to_submission(self, submission, result_text):
        """process a new reddit message, reply to it, add it to log

        :submission: submission to process
        :result_text: the result of a message

        """

        if result_text:
            print("post {} is being processed".format(submission.id))
            print("\nPOST*********************")
            # print first 1000 characters
            print(result_text[:1000])
            print("POST_END*********************\n")

            if not self.debug:
                # reply to submission
                submission.reply(result_text)
                # add submission to post log
                self.post_log.add(submission.id)

            print("Part of post_log: ")
            self.post_log.print_posts()
            print("\n-------------------\n")

    @staticmethod
    def format_reddit_text(text):
        """format text into reddit block quote

        :text: text to add to a comment
        :returns: formatted text to add to a result, or None

        """

        if not text or len(text) <= 1 or text.isspace():
            # if the text length is too short or blank
            # return no text found message
            # return "{message}\n\n".format(message=NO_TEXT_FOUND)
            return None

        # remove text leading and trailing whitespace if they exist
        text = text.lstrip().rstrip()

        # split text into lines
        text_lines = text.splitlines()

        final_text = ">"
        prev_is_space = False

        for line in text_lines:
            if line == "" or line.isspace():
                # if the current line is whitespace
                if prev_is_space:
                    # if the previous line was whitespace
                    continue
                prev_is_space = True
                final_text += "\n>\n>"
            else:
                # if the previous line is not whitespace, add a space and the
                # line set prev_is_space to false
                final_text += " " + line
                prev_is_space = False

        # add a final 2 newlines
        final_text += "\n\n"

        return final_text

    @staticmethod
    def get_reddit_message_text(img_urls, post_url,
                                max_length=MAX_REPLY_LENGTH):
        """Get reddit message result text

        :img_urls: list of image urls
        :post_url: post url
        :max_length: maximum length for reply
        :returns: full reddit message text, or None

        """

        if not post_url or not img_urls:
            return None

        none_count = 0
        char_count = 0

        result_text = ""

        # if urls is not empty
        for url in img_urls:
            # if the added text is greater than the max reply length allowed
            if char_count >= max_length:
                break

            url_text = get_image_text(url)

            if not url_text:
                # if there is not url text, continue and increment
                # none_count
                none_count += 1
                continue

            formatted_text = Bot.format_reddit_text(url_text)
            result_text += formatted_text
            char_count += len(formatted_text)

        if none_count >= len(img_urls):
            # if the messages with none are greater or equal to the length of
            # the image urls
            return None

        # strip excess whitespace and limit length of result
        result_text = result_text.lstrip().rstrip()
        result_text = result_text[:max_length]

        # add text header and footer
        result_text = "{header} [{url}]({url})\n{content}\n\n{footer}".format(
            url=post_url, header=BOT_HEADER, content=result_text,
            footer=BOT_FOOTER)

        return result_text
