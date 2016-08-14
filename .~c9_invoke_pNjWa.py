# works with edgarfilings 
from edgarfilings import edgarfilings
import csv
import sys
import datetime
# arg - filename of CIK list
# arg - filename of CIK list
if len(sys.argv) < 2:
    print "Syntax: ", sys.argv[0], "input_filename"
else:    
    ciklist=[]
    with open(sys.argv[1], 'rb') as mgrslist:
        mgrreader = csv.reader(mgrslist, dialect='excel')
        for row in mgrreader:
            ciklist.append(row)
            
    cik_counter = 0        
    edgar=managerfilings()
    print datetime.datetime.now()
    for line in ciklist:    
        k=line[0]
        print " - ".join([str(cik_counter), str(k).zfill(10)])
        filing = edgar.get_filing_as_list(str(k).zfill(10))
        if len(filing)>1:
            rpt_date = filing[1][2]
            out_file = "./output/13F_"+rpt_date+".txt"
            # write header
            if cik_counter == 0:
                writer = csv.writer(open(out_file,"wb"), dialect='excel', quoting=csv.QUOTE_ALL)        
                writer.writerow(filing[0])        
            cik_counter += 1
            print " - ".join([filing[1][0], rpt_date, str(len(filing))])
            # write out the results
            writer = csv.writer(open(out_file,"ab"), dialect='excel', quoting=csv.QUOTE_ALL)
            for holding in filing[1:]:          
                writer.writerow(holding)
    print datetime.datetime.now()