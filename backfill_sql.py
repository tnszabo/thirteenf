import thirteenf_sql as db
import getedgarfiling as ed
import datetime
import pandas as pd

# get cik from db
ciklist = db.getMgrCiks()

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
                        #convert to dataframe and append flattened holdings
                        df1 =  pd.DataFrame(myfiling)
                        df1.drop('holdings', axis=1, inplace=True)
                        df2 = pd.DataFrame(myfiling['holdings'])
                        df3 = pd.concat([df1, df2], axis=1)
                        if not df3.empty:
                            db.appendFilings(df3) 
                            print 'Filing:', myfiling['periodofreport'], myfiling['tableentrytotal'], myfiling['manager_name']
                            ctrHoldings += myfiling['tableentrytotal']

tFinish = datetime.datetime.now() - start     
print "Batch:", start, "Run time:", tFinish, "Holdings:", ctrHoldings, "Rate:", ctrHoldings/tFinish.total_seconds()

# get summary report of managers by date
c = pd.read_sql_query(
    "select distinct cik, periodofreport, tableentrytotal from filings order by 1", db.getDbConn())
print pd.pivot_table(c, index = ['cik'], columns = ['periodofreport'])