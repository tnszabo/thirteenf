# works with getEdgar13fv 5 or 6
from getEdgar13fv6 import Cik
import csv
import sys
import datetime
# arg - filename of CIK list
# create instance of Cik
if len(sys.argv) < 2:
    print "Syntax: ", sys.argv[0], "input_filename"
else:    
    ticker=Cik()
    cik_counter = 0
    ciklist=[]
    with open(sys.argv[1], 'rb') as mgrslist:
        mgrreader = csv.reader(mgrslist, dialect='excel')
        for row in mgrreader:
            ciklist.append(row)
    print datetime.datetime.now()
    for line in ciklist:    
        k=line[0]
        filing = ticker.process_cik(str(k).zfill(10))
        if filing is not None:
            rpt_date = filing[0][2]
            out_file = "./output/13F_"+rpt_date+".txt"
            if cik_counter == 0:
                writer = csv.writer(open(out_file,"wb"), dialect='excel', quoting=csv.QUOTE_ALL)        
                header = []
                header.append("Manager")
                header.append("MgrCik")
                header.append("Period")             
                header.append("CUSIP")
                header.append("Name")
                header.append("Value")
                header.append("Shares")
                header.append("Class")
                header.append("PutCall")
                writer.writerow(header)        
            cik_counter += 1
            print " - ".join([str(cik_counter), str(k).zfill(10), filing[0][0], rpt_date, str(len(filing))])
            # write out the results
            writer = csv.writer(open(out_file,"ab"), dialect='excel', quoting=csv.QUOTE_ALL)
            for holding in filing:          
                writer.writerow(holding)
    print datetime.datetime.now()




