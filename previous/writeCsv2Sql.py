import pandas as pd
import sqlite3

file = "../output/13F_12-31-2015.txt"
frame = pd.read_csv(file, skipinitialspace=True)
print 'Len-',len(frame)

# consolidate names
grouped = frame.groupby(['Period','Manager','MgrCik','CUSIP','Name','PutCall','Class']).sum()
# upload to database
sqlite_file = '../thirteenf_db.sqlite'    # name of the sqlite database file
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
grouped.to_sql('filings', conn, flavor='sqlite', if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
conn.commit()
conn.close()