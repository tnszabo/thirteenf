import getedgarfiling as ed
import csv
import sys
import datetime
from pymongo import MongoClient

# input arg - filename of CIK list
if len(sys.argv) < 2:
    print "Syntax: ", sys.argv[0], "input_filename"
else:    
    ciklist=[]
    with open(sys.argv[1], 'rb') as mgrslist:
        mgrreader = csv.reader(mgrslist, dialect='excel')
        for row in mgrreader:
            ciklist.append(row[0])
    
    # connect to mongodb
    connection = MongoClient()    
    db = connection.thirteenfdb.thirteenf
    
    # iterate over cik list
    cik_counter = 0        
    filing = ''
    start =  datetime.datetime.now()
    for k in ciklist:    
        cik = str(k).zfill(10)
        available = ed.get_filings_available(cik)
        for k in available.iterkeys():
            j = ed._get_filing_as_json(available[k])
            #insert to mongo db
            db.insert(j)

        cik_counter+=1
         
    print datetime.datetime.now() - start
        