import sqlite3
from _config import DATABASE_PATH


with sqlite3.connect(DATABASE_PATH) as sql_connection:

    cursor = sql_connection.cursor()

    cursor.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name TEXT NOT NULL,
                                        due_date TEXT NOT NULL,
                                        priority INTEGER NOT NULL,
                                        status INTEGER NOT NULL)""")

    cursor.execute("""INSERT INTO tasks(name, due_date, priority, status)
                        VALUES("Finish this tutorial",
                        "03/25/2015",
                        10,
                        1)""")
    cursor.execute("""INSERT INTO tasks(name, due_date, priority, status)
                        VALUES("Finish Real Python Course 2",
                        "03/25/2015",
                        10,
                        1)""")
