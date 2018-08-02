"""Contains PRAW reddit bot code"""

from imgur import is_url_imgur, get_imgur_urls
from reddit import is_url_reddit, get_reddit_urls
from ocr import get_image_text
import config
import praw

BOT_HEADER = "#Transcribe_bot\n*****"
BOT_FOOTER = ("Powered by transcribe_bot. " +
              "[Github](https://github.com/isaaclo123/transcriber_bot)")
NO_TEXT_FOUND = "*No text found*"

def format_reddit_text(text, count):
    """Add to result text

    :text: text to add to a comment
    :count: header page number
    :returns: formatted text to add to a result

    """

    if len(text) <= 1 or text.isspace():
        # if the text length is too short or blank
        # return "no text found"
        return "##{header}\n{message}\n\n".format(header=count,
                                                  message=NO_TEXT_FOUND)

    # remove text leading and trailing whitespace if they exist
    text = text.lstrip().rstrip()

    # split text into lines
    text_lines = text.splitlines()

    print(text_lines)

    final_text = "##{header}\n>".format(header=count)
    prev_is_space = False

    for line in text_lines:
        if line.isspace():
            if prev_is_space:
                # if the previous line is whitespace, skip
                continue
            else:
                # add a single newline and set prev_is_space to true
                prev_is_space = True
                final_text += "\n>"
        else:
            # if the previous line is not whitespace, add a space and the line
            # set prev_is_space to false
            final_text += " {}".format(line)
            prev_is_space = False

    # add a final 2 newlines
    final_text += "\n\n"

    return final_text

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
        print("url: {url}".format(url=url))
        img_urls = []

        if is_url_imgur(url):
            # if url is imgur
            img_urls = get_imgur_urls(url)
        elif is_url_reddit(url):
            img_urls = get_reddit_urls(url)
        else:
            # url invalid
            print("url invalid, skipping")
            img_urls = []

        print(img_urls)

        result_text = "{}\n".format(BOT_HEADER)

        if img_urls:
            # if urls is not empty
            url_count = 1
            for url in img_urls:
                url_text = get_image_text(url)
                result_text += format_reddit_text(url_text, url_count)
                url_count += 1
        else:
            result_text = NO_TEXT_FOUND

        result_text += BOT_FOOTER

        print(result_text)

if __name__ == '__main__':
    main()
