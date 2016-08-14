import sqlite3

sqlite_file = '../thirteenf_db.sqlite'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute('SELECT * FROM managers')
print c
conn.close()