import sqlite3


with sqlite3.connect("db.sql") as connection:
    c = connection.cursor()

    c.execute("""CREATE TABLE posts
                (title TEXT, post TEXT)
                """)
    c.executemany('INSERT INTO posts VALUES(?,?)', [
                ("Good", r"I'm good."),
                ("Well", r"I'm well.")
                ])
    