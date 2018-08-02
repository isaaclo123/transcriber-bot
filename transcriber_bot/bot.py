"""Contains PRAW reddit bot code"""

from imgur import is_url_imgur, get_imgur_urls
from reddit import is_url_reddit, get_reddit_urls
from ocr import get_image_text
import config
import praw

BOT_FOOTER = ("Powered by transcribe_bot. " +
              "[Github](https://github.com/isaaclo123/transcriber_bot)")

def result_text_add(text, count):
    """Add to result text

    :text: text to add to a comment
    :count: header page number
    :returns: formatted text to add to a result

    """

    if len(text) <= 1 or text.isspace():
        # if the text length is too short or blank
        # return "no text found"
        return "##{header}\n*No text found*\n\n".format(header=count)

    # remove text trailing newline if it exists
    if text[-2:] == "\n":
        text = text[:-2]

    # add quotes after all newlines and adds quote to first line
    # ex: "hi\nbye" turns into ">hi\n>bye"
    text = text.replace("\n", "\n>")
    text = text.replace("\n", "\n>")
    # adds header to beginning and newline to end
    return "##{header}\n>{text}\n\n".format(header=count, text=text)

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

        result_text = ""

        if img_urls:
            # if urls is not empty
            url_count = 1
            for url in img_urls:
                url_text = get_image_text(url)
                result_text += result_text_add(url_text, url_count)
                url_count += 1
        else:
            result_text = "*No text found*"

        result_text += BOT_FOOTER

        print(result_text)

if __name__ == '__main__':
    main()
