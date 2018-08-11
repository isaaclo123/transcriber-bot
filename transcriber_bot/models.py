"""Contains db code"""

import sqlite3
import os

DEFAULT_MAX_LOG_LENGTH = 100
DEFAULT_MAX_POST_LENGTH = 6
CUR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(CUR_PATH, "postlog.db")

class PostLog(object):
    """Class for logging transcribe bot posts"""

    def __init__(self, max_log_len=DEFAULT_MAX_LOG_LENGTH,
                 max_post_len=DEFAULT_MAX_POST_LENGTH):
        """constructor for PostLog

        :max_log_len: max length for log to be

        """
        self.conn = sqlite3.connect(DB_FILE)

        self.cur = self.conn.cursor()
        self.max_log_len = max_log_len
        self.max_post_len = max_post_len

        # create table for stored iterator variable
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS vars (
            id char(1) PRIMARY KEY,
            val int({})
        )""".format(str(self.max_log_len)))

        # initialize iterator variable i if needed
        self.cur.execute("""
        INSERT OR IGNORE INTO vars(id, val) VALUES('i', 0)
        """)

        # create table
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id int({}) NOT NULL PRIMARY KEY,
            post char({})
        )""".format(str(self.max_log_len), str(self.max_post_len)))


    def add(self, post):
        """adds post to PostLog

        :post: string with post id
        :returns: same post id if item added, None if item exists in PostLog
        already

        """
        if self.is_in(post):
            # if the item is in the PostLog already, do nothing
            return None

        # add post at id = i
        self.cur.execute("""
        REPLACE INTO posts(id, post)
            VALUES(
                (SELECT val FROM vars WHERE id='i' LIMIT 1),
                ?
        )""".format(str(self.max_log_len)), (post,))

        # increment iterator variable by 1, loop at 100
        self.cur.execute("""
        UPDATE vars
        SET val=(((SELECT val FROM vars WHERE id='i' LIMIT 1) + 1) % {})
        WHERE id='i'
        """.format(str(self.max_log_len)))

        # commit changes
        self.conn.commit()

        return post

    def is_in(self, post):
        """returns if a post is in the post log

        :post: string with post id
        :returns: true if post is in PostLog, and false otherwise

        """
        self.cur.execute("SELECT 1 FROM posts WHERE post=?", (post,))
        # return if there are one or more results from the post query
        return len(self.cur.fetchall()) > 0

    def print_posts(self):
        """prints posts"""
        self.cur.execute("SELECT * FROM posts")
        print(self.cur.fetchall())
