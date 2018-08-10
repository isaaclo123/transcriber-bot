"""Contains db code"""

import sqlite3

DEFAULT_MAX_LOG_LENGTH = 100
DB_FILE = "postlog.db"

class PostLog(object):
    """Class for logging transcribe bot posts"""

    def __init__(self, max_length=DEFAULT_MAX_LOG_LENGTH):
        """constructor for PostLog

        :max_length: max length for log to be

        code taken from https://www.xaprb.com/blog/2007/01/11/
        how-to-implement-a-queue-in-sql/
        """
        conn = sqlite3.connect(DB_FILE)
        self.max_length = max_length
        self.db = conn.cursor

        # create queue
        self.db.execute("""
                        CREATE TABLE IF NOT EXISTS posts (
                            id int NOT NULL,
                            modulo int NOT NULL,
                            post_id varchar(10) NOT NULL,
                            PRIMARY KEY(id),
                            UNIQUE KEY(modulo)
                        )
                        """)

    def add(self, post_id):
        """adds post to PostLog

        :post_id: string with post id
        :returns: same post id if item added, None if item exists in PostLog
        already

        """
        if self.is_in(post_id):
            # if the item is in the PostLog already, do nothing
            return None

        self.db.execute("""
                        INSERT INTO posts(id, modulo, post)
                        SELECT
                            (coalesce(max(id), -1) + 1),
                            (coalesce(max(id), -1) + 1) mod ?,
                            ?
                        FROM posts
                            ON DUPLICATE KEYU UPDATE
                                id = values(id),
                                post = values(post)
                        """, self.max_length, post_id)
        return post_id

    def is_in(self, post_id):
        """

        :post_id: string with post id
        :returns: true if post is in PostLog, and false otherwise

        """
        self.db.execute("SELECT * FROM posts WHERE post_id=?", post_id)
        # return if there are one or more results from the post_id query
        return len(self.db.fetchall()) > 0
