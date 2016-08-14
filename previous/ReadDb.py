import pandas as pd
import numpy as np

import sqlite3
sqlite_file = '../thirteenf_db.sqlite'    # name of the sqlite database file
conn = sqlite3.connect(sqlite_file)

sqlstmt = 'select * from filings'
df2 = pd.read_sql_query(sqlstmt, conn)

print df2.columns.values
print df2.index.values
# append this code to getMgrFilings before loading to database

# add exposure column to the df
#pivotMgr = pd.pivot_table(df2, index = ['Period','Manager','MgrCik','CUSIP','Name','PutCall'], values=['Value']) 
#print pivotMgr.head()
#pivotMgr['Exposure'] = pivotMgr.groupby(level = 2).transform(lambda x: x/x.sum())
#print pivotMgr.head()
#print pivotMgr.describe()

#new = pd.merge(df2, pivotMgr)
#print new
#pivotMgr = pd.pivot_table(df2, \
#    index = ['MANAGER'], values = ['Value'], aggfunc = np.sum) 
#print pivotMgr