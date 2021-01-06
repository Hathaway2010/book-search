import sqlite3

conn = sqlite3.connect("inventory.db")
c = conn.cursor()
c.execute("DROP TABLE inv")
