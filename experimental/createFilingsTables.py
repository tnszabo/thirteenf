# deprecated!
# now merged into thirteenfdb

import sqlite3
sqlite_file = 'thirteenf_db.sqlite'    # name of the sqlite database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
# create tables


c.execute('CREATE TABLE filings \
        (    Period DATE NOT NULL,\
        MANAGER VARCHAR(64) NOT NULL,\
        MgrCik VARCHAR(10) NOT NULL,\
        CUSIP VARCHAR(9) NOT NULL, \
        Name VARCHAR(64),\
        Class VARCHAR(8),\
        PutCall VARCHAR(8),\
        Value DECIMAL(10,2) NOT NULL,\
        Shares INTEGER NOT NULL,\
        Pct_Filing DECIMAL(10,2),\
        PRIMARY KEY (MANAGER, MgrCik, Period, CUSIP, Class, PutCall))')
conn.commit()

conn.close()