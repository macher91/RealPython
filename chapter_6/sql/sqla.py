import sqlite3


con = sqlite3.connect("new.db")
cursor = con.cursor()
cursor.execute("""CREATE TABLE population
                    (city TEXT, state TEXT, population INT)
                    """)
con.close()
