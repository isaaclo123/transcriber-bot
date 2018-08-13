"""Contains PRAW reddit bot code"""

import praw
from transcriber_bot.imgur import is_url_imgur, get_imgur_urls
from transcriber_bot.reddit import is_url_reddit, get_reddit_urls
from transcriber_bot.ocr import get_image_text

BOT_FOOTER = ("Powered by [transcriber_bot]" +
              "(https://github.com/isaaclo123/transcriber_bot), /u/isaac_lo")
CONTINUED_MSG = "cont."
MAX_COMMENT_LENGTH = 10000

class Bot(object):
    """Class for transcriber bot"""

    # set "initialized" marker to false
    initialized = False

    def __init__(self, post_log, config):
        """initializes Bot

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

    def run(self):
        """runs bot

        :raises: RuntimeException saying bot is not initialized

        """
        if not self.initialized:
            raise RuntimeError('Bot not initialized')

        # loop through submissions in subreddit stream
        for submission in self.subreddits.submissions():
            if self.post_log.is_in(submission.id):
                # if the post id is already in the post log, skip processing
                print("post {} has already been processed".format(
                    submission.id))
                continue

            url = submission.url
            img_urls = []

            if is_url_imgur(url):
                # if url is imgur
                img_urls = get_imgur_urls(url)
            elif is_url_reddit(url):
                img_urls = get_reddit_urls(url)
            else:
                # url invalid
                img_urls = []

            result_text = Bot.get_reddit_message_text(img_urls, url)
            result_text_list = Bot.split_reddit_message(result_text)

            to_reply = submission

            if result_text:
                print("post {} is being processed".format(submission.id))
                print("message will be split into {} posts".format(
                    len(result_text_list)))
                print("\nPOST*********************")
                # print first 1000 characters
                print(result_text[:1000])
                print("POST_END*********************\n")

                if not self.debug:
                    for result in result_text_list:
                        # keep nesting result_text_list responses with replies
                        to_reply = to_reply.reply(result)

                    # add submission to post log
                    self.post_log.add(submission.id)

                print("Part of post_log: ")
                self.post_log.print_posts()
                print("\n-------------------\n")

    @staticmethod
    def format_reddit_text(text):
        """Add to result text

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
    def get_reddit_message_text(img_urls, post_url):
        """Get reddit message result text

        :img_urls: list of image urls
        :post_url: optional argument for post url
        :returns: full reddit message text, or None

        """
        # add text header
        result_text = "A text transcription of [{url}]({url})\n".format(
            url=post_url)

        none_count = 0

        if img_urls:
            # if urls is not empty
            for url in img_urls:
                url_text = get_image_text(url)

                if not url_text:
                    # if there is not url text, continue and increment
                    # none_count
                    none_count += 1
                    continue

                result_text += Bot.format_reddit_text(url_text)
        else:
            # returns None if img_urls is empty or invalid
            return None

        if none_count >= len(img_urls):
            # if the messages with none are greater or equal to the length of
            # the image urls
            return None

        result_text += BOT_FOOTER

        return result_text

    @staticmethod
    def split_reddit_message(msg):
        """splits reddit message result text to list of maximum comment size

        :msg: message to split
        :returns: list of reddit message text. It is a list of strings that have
        a maximum length of MAX_COMMENT_LENGTH

        """
        if not msg:
            return []

        msg_list = []

        if len(msg) <= MAX_COMMENT_LENGTH:
            return [msg]

        while msg:
                # in the event that the message would be cut off
            if (MAX_COMMENT_LENGTH < len(msg) <
                    MAX_COMMENT_LENGTH+len(BOT_FOOTER)):
                # remove bot footer and add to msg_list
                msg_list.append(msg[:-1*len(BOT_FOOTER)].lstrip().rstrip())
                # add bot footer in seperate message
                msg_list.append(BOT_FOOTER)
                break

            # get message segment from list and left strip it
            msg_item = msg[0:MAX_COMMENT_LENGTH].lstrip()
            # get last word (or word part) in msg_item
            msg_item_final_char = msg_item.split()[-1]
            # remove that last word (or part or word) from msg_item
            msg_item = msg_item[:-1*len(msg_item_final_char)]
            # append that to msg_list
            msg_list.append(msg_item)
            # set msg to be the rest of the text, with the last word from the
            # msg_item added on, only if the last item is not the entire
            # msg_item
            if len(msg_item_final_char) < len(msg_item):
                msg = (msg_item_final_char + msg[MAX_COMMENT_LENGTH:]).lstrip()
            else:
                msg = msg[MAX_COMMENT_LENGTH:].lstrip()

            if msg and msg[0] != ">":
                # is msg exists and there is no carat (reddit blockquote) to
                # begin the message, add one to msg
                msg = ">" + msg

            # add continued message
            msg = "{cont}\n{msg}".format(cont=CONTINUED_MSG, msg=msg)

        return msg_list
