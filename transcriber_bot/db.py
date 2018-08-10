"""Contains db code"""

import sqlite3

DEFAULT_MAX_LOG_LENGTH = 100
MAX_POST_LENGTH = 6
DB_FILE = "postlog.db"

class PostLog(object):
    """Class for logging transcribe bot posts"""

    def __init__(self, max_length=DEFAULT_MAX_LOG_LENGTH):
        """constructor for PostLog

        :max_length: max length for log to be

        """
        self.conn = sqlite3.connect(DB_FILE)

        self.db = self.conn.cursor()
        self.max_length = max_length

        # create table for stored iterator variable
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS vars (
            id char(1) PRIMARY KEY,
            val int({})
        )""".format(str(self.max_length)))

        # initialize iterator variable i if needed
        self.db.execute("""
        INSERT OR IGNORE INTO vars(id, val) VALUES('i', 0)
        """)

        # create table
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id int({}) NOT NULL PRIMARY KEY,
            post char({})
        )""".format(str(self.max_length), str(MAX_POST_LENGTH)))


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
        self.db.execute("""
        REPLACE INTO posts(id, post)
            VALUES(
                (SELECT val FROM vars WHERE id='i' LIMIT 1),
                ?
        )""".format(str(self.max_length)), (post,))

        # increment iterator variable by 1, loop at 100
        self.db.execute("""
        UPDATE vars
        SET val=(((SELECT val FROM vars WHERE id='i' LIMIT 1) + 1) % {})
        WHERE id='i'
        """.format(str(self.max_length)))

        # commit changes
        self.conn.commit()

        return post

    def is_in(self, post):
        """returns if a post is in the post log

        :post: string with post id
        :returns: true if post is in PostLog, and false otherwise

        """
        self.db.execute("SELECT 1 FROM posts WHERE post=?", (post,))
        # return if there are one or more results from the post query
        return len(self.db.fetchall()) > 0

    def print_posts(self):
        """prints posts"""
        self.db.execute("SELECT * FROM posts")
        print(self.db.fetchall())
