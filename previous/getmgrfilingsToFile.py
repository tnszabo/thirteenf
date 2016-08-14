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
        # get filing report 
        filing = ed.get_filing_as_list(str(k).zfill(10))
        if filing is not None:
            if cik_counter == 0:
                # first time through
                rpt_date = filing[1][2]
                out_file = "./output/13F_"+rpt_date+".txt"
                # output - write filing to out_file
                # write header
                writer = csv.writer(open(out_file,"wb"), dialect='excel', quoting=csv.QUOTE_ALL)        
                writer.writerow(filing[0])        
            # write out the rows
            writer = csv.writer(open(out_file,"ab"), dialect='excel', quoting=csv.QUOTE_ALL)
            for holding in filing[1:]:          
                writer.writerow(holding)    
            cik_counter+=1
            print " - ".join([filing[1][0], str(len(filing))])
    print datetime.datetime.now() - start