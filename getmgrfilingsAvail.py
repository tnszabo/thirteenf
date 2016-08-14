import getedgarfiling as ed
import csv
import sys
import datetime

# input arg - CIK
if len(sys.argv) < 2:
    print "Syntax: ", sys.argv[0], "cik"
else:    
    cik = sys.argv[1]
    start =  datetime.datetime.now()
    filings = ed.get_filings_available(str(cik).zfill(10))
    
    # output - list of filings dates and urls
    for period in sorted(filings):
        print period, filings[period]
    print datetime.datetime.now() - start