"""Contains PRAW reddit bot code"""

from imgur import is_url_imgur, get_imgur_urls
from reddit import is_url_reddit, get_reddit_urls
from ocr import get_image_text
import config
import praw

# BOT_HEADER = "###Transcriber_bot"
BOT_FOOTER = ("Powered by transcriber_bot. " +
              "[Github](https://github.com/isaaclo123/transcriber_bot)")
NO_TEXT_FOUND = "*No text found*"
DEBUG = True

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
            # if the previous line is not whitespace, add a space and the line
            # set prev_is_space to false
            final_text += " {}".format(line)
            prev_is_space = False

    # add a final 2 newlines
    final_text += "\n\n"

    return final_text

def get_reddit_message_text(img_urls, post_url):
    """Get reddit message message result text

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
                # if there is not url text, continue and increment none_count
                none_count += 1
                continue

            result_text += format_reddit_text(url_text)
    else:
        # returns None if img_urls is empty or invalid
        return None

    if none_count >= len(img_urls):
        # if the messages with none are greater or equal to the length of the
        # image urls
        return None

    result_text += BOT_FOOTER

    return result_text

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
        print("no subreddits in list")
        return

    # otherwise create subreddits stream string
    subreddit_stream = subreddit_list[0]
    for i in range(1, len(subreddit_list)):
        subreddit_stream += "+{subreddit}".format(subreddit=subreddit_list[i])

    subreddits = reddit.subreddit(subreddit_stream).stream

    # loop through submissions in subreddit stream
    for submission in subreddits.submissions():
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

        result_text = get_reddit_message_text(img_urls, url)

        if result_text:
            print(result_text)
            if not DEBUG:
                submission.reply(result_text)
            print("\n-------------------\n")

if __name__ == '__main__':
    main()
