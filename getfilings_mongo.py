import getedgarfiling as ed
import datetime
import thirteenf_mongo as db

conn = db.getDbConn()
dbf = conn.filings
dbm = conn.managers

# get list of managers
ciklist = dbf.distinct("cik")
if not ciklist:
    ciklist = dbm.distinct("cik")
print "Manager ciks:", ciklist

# calculate last quarter end date
lastPeriod = ed.previous_quarter(datetime.datetime.today() - datetime.timedelta(days=45))
print 'Closest quarter end', lastPeriod

# iterate over cik list
filing = ''
print 'ciks:', len(ciklist)
ctrHoldings = 0
start =  datetime.datetime.now()
for cik in ciklist:    
    if dbf.find({"cik":cik, "periodofreport":lastPeriod}).limit(1).count() == 0:
        myfiling = ed.get_filing_as_json(cik)
        
        if myfiling['periodofreport']==lastPeriod:
            myfiling['batch']=start
            
            dbf.insert(myfiling)
            print 'Filing:', myfiling['periodofreport'], myfiling['tableentrytotal'], myfiling['manager_name']
            ctrHoldings += myfiling['tableentrytotal']
     
tFinish = datetime.datetime.now() - start     
print "Batch:", start, "Run time:", tFinish, "Holdings:", ctrHoldings, "Rate:", ctrHoldings/tFinish.total_seconds()