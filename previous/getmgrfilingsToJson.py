import getedgarfiling as ed
import csv
import sys
import datetime

# input arg - filename of CIK list
if len(sys.argv) < 2:
    print "Syntax: ", sys.argv[0], "input_filename"
else:    
    ciklist=[]
    with open(sys.argv[1], 'rb') as mgrslist:
        mgrreader = csv.reader(mgrslist, dialect='excel')
        for row in mgrreader:
            ciklist.append(row[0])
    # iterate over cik list
    cik_counter = 0        
    filing = ''
    start =  datetime.datetime.now()
    for k in ciklist:    
        print " - ".join([str(cik_counter), str(k).zfill(10)])
        
        #output - filings 
        print ed.get_filing_as_json(str(k).zfill(10))
         
    print datetime.datetime.now() - start