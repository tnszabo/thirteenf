import thirteenfdb as db
import getedgarfiling as ed
import fidelity
import datetime
import pandas as pd
import csv
import sys
from pandas.io.json import json_normalize

def previous_quarter(ref):
    if ref.month < 4:
        return datetime.date(ref.year - 1, 12, 31)
    elif ref.month < 7:
        return datetime.date(ref.year, 3, 31)
    elif ref.month < 10:
        return datetime.date(ref.year, 6, 30)
    return datetime.date(ref.year, 9, 30)
    
def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[str(name[:-1])] = str(x)
    flatten(y)
    return out

# pseudo-code
# 1. get a list of MgrCiks from managers table or filings table or union of both
# 2. calculate last quarter end date
# 3. 

# get list of MgrCiks from db
df = db.getMgrCiks()
print df
ciklist = df['MgrCik']

# calculate last quarter end date
adjToday = datetime.datetime.today() - datetime.timedelta(days=45) 
prev = previous_quarter(adjToday)
lastPeriod = prev.strftime('%m-%d-%Y')
print 'closest quarter end', lastPeriod

# cik = '1137521'
# myfiling = ed.get_filing_as_json(cik)
# #convert to dataframe and append flattened holdings
# df1 =  pd.DataFrame(myfiling)
# df1.drop('holdings', axis=1, inplace=True)
# #df2 =  json_normalize(myfiling['holdings'])
# df2 = pd.DataFrame(myfiling['holdings'])
# #final for load to database
# final = pd.concat([df1, df2], axis=1)
# print final
final = pd.DataFrame()
start =  datetime.datetime.now()

for cik in ciklist:
    if not db.getFilingCountByPeriod(cik, lastPeriod):
        myfiling = ed.get_filing_as_json(cik)
        print 'insert filing:',cik, myfiling['tableentrytotal']
        #convert to dataframe and append flattened holdings
        df1 =  pd.DataFrame(myfiling)
        df1.drop('holdings', axis=1, inplace=True)
        df2 = pd.DataFrame(myfiling['holdings'])
        df3 = pd.concat([df1, df2], axis=1)
        final= final.append(df3, ignore_index=True)
    
    if not db.getFilingCountByPeriod(cik, lastPeriod):

print datetime.datetime.now() - start