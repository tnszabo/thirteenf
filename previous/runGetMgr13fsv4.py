from getEdgar13fv4 import Cik
import csv
import sys

managers=[]

with open(sys.argv[1], 'rb') as mgrslist:
    mgrreader = csv.reader(mgrslist, dialect='excel')
    for row in mgrreader:
        managers.append(row)

# create instance of Cik with list of managers as argument
# works with getEdgar13fv4
ticker=Cik(managers)
ticker.process_cik_list()
