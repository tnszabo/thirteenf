import thirteenfdb as db
import getedgarfiling as ed
import fidelity

import datetime
import pandas as pd
import csv
import sys

ciklist=[]

# read command line arg
if len(sys.argv) > 1:
    with open(sys.argv[1], 'rb') as mgrslist:
        mgrreader = csv.reader(mgrslist, dialect='excel')
        for row in mgrreader:
            ciklist.append(row[0])
print datetime.da
# or get list of MgrCiks from db
if len(ciklist) == 0:
    dfDbFlngs = db.getMgrCikPeriods() 
    ciklist = dfDbFlngs['MgrCik'].values.tolist()
    print dfDbFlngs.max()
    print dfDbFlngs.groupby('Period').get_group('03-31-2016')
    
if len(ciklist) == 0:
    print "No managers cik found."
else:
    #clear tempfilings table
    db.delFilings()
    cik_counter = 0        
    start = datetime.datetime.now()
    for cik in ciklist:    
        cik_counter += 1
        
        print db.getMgrFilings(str(cik).zfill(10))
        filing = ed.get_filing_as_df(str(cik).zfill(10))
        
        #print len(filing.index)
        #if len(filing.index)>1:
        print " - ".join([ filing.index.values[0][1], filing.index.values[0][0], str(len(filing.index)) ])
        # save to database
        try: 
            db.AppendTempFilings(filing)
        except Exception, e:
            print "Error on insert: %s" % e
            pass
            
    print datetime.datetime.now() - start
            
    # insert names and symbols        
    names = fidelity.getSymbols(db.getCusips())  
    print len(names.index)
    try: 
        db.AppendNames(names)  
    except Exception, e:
        print "AppendNames: Error: %s" % e
        pass
    
    # insert into filings
    db.insertFilings()
    
    # export filings to csv
    db.getFilings().to_csv('filings.csv', index = False)
    
    print datetime.datetime.now() - start