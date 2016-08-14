import lib.thirteenf_sql as db
import lib.getedgarfiling as ed
import datetime
import pandas as pd

# pseudo-code
# 1. get a list of MgrCiks from managers table or filings table or union of both
# 2. calculate last quarter end date
# 3. for each cik in MgrCiks
# 4.    db lookup filings for cik, last quarter
# 5.    if false, get edgar filings for cik, 
# 6.    if filing is for last quarter, save

# get list of MgrCiks from db
ciklist = db.getMgrs()
print 'ciks:', len(ciklist)
# calculate last quarter end date
lastPeriod = ed.previous_quarter(datetime.datetime.today() - datetime.timedelta(days=45))
print 'Closest quarter end', lastPeriod
ctrHoldings = 0
start =  datetime.datetime.now()
for cik in ciklist:
    if not db.existsFiling(cik, lastPeriod):
        myfiling = ed.get_filing_as_json(cik)
        if myfiling:
            if myfiling['periodofreport']==lastPeriod:
                
                df1 =  pd.DataFrame(myfiling)
                df1.drop('holdings', axis=1, inplace=True)
                df2 = pd.DataFrame(myfiling['holdings'])
                flattened = pd.concat([df1, df2], axis=1)
        
                if not flattened.empty:
                    db.appendFilings(flattened)
                    print 'Filing:', myfiling['periodofreport'], myfiling['tableentrytotal'], myfiling['manager_name']#convert to dataframe and append flattened holdings
                    ctrHoldings += myfiling['tableentrytotal']
    else:  
        print cik, "No new filings found"
tFinish = datetime.datetime.now() - start     
print "Batch:", start, "Run time:", tFinish, "Holdings:", ctrHoldings, "Rate:", ctrHoldings/tFinish.total_seconds()

print db.getFilingSummary(lastPeriod)