import thirteenf_mongo as db
import getedgarfiling as ed
import datetime
import pandas as pd
from pymongo import MongoClient

# get list of ciks from db
conn = db.getDbConn()
dbf = conn.filings
dbm = conn.managers

# get list of managers
ciklist = dbf.distinct("cik")
if not ciklist:
    ciklist = dbm.distinct("cik")
print ciklist
ctrHoldings = 0
start =  datetime.datetime.now()
if not ciklist:
    print "No new managers"
    exit
else:
    for cik in ciklist:
        urls = ed.get_urls_available(cik)
        if not urls.empty:
            for fdate in urls.index:
                if not db.existsFiling(cik, fdate):
                    myfiling = ed._xml_tojson(ed._get_xml(urls[fdate][0]))
                    if myfiling:
                        myfiling['batch']=start
                        db.appendFilings(myfiling)
                        print 'Filing:',cik, myfiling['periodofreport'], myfiling['tableentrytotal']
                        ctrHoldings += myfiling['tableentrytotal']

tFinish = datetime.datetime.now() - start     
print "Batch:", start, "Run time:", tFinish, "Holdings:", ctrHoldings, "Rate:", ctrHoldings/tFinish.total_seconds()

conn = MongoClient()   
flngs = conn.thirteenfdb.filings
fl = flngs.find({}, {"periodofreport":1, "cik":1, "_id":0, "tableentrytotal":1})
c = pd.DataFrame(list(fl))
pivot = pd.pivot_table(c, index = ['cik'], columns = ['periodofreport'])
print pivot