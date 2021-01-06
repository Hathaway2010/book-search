import sqlite3
from sys import argv, exit

if len(argv) != 2:
    print("Usage: python query.py database.db")
    exit(1)

conn = sqlite3.connect(argv[1])
c = conn.cursor()
rows = c.execute("SELECT * FROM inv")
for row in rows:
    print(row)
