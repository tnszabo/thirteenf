import thirteenf_sql as db
import fidelity_v2 as fidelity
import datetime
import pandas as pd

c = db.getNewCusips()
print "New cusips:", len(c)

start = datetime.datetime.now()
        
# get names and symbols  
names = fidelity.getSymbols(c)  

print "Run time:", datetime.datetime.now() - start

print "New symbols:", len(names.index)
if len(names.index)>0:
    try: 
        print names
        db.appendNames(names)  
    except Exception, e:
        print "appendNames:", e
    pass

tFinish = datetime.datetime.now() - start     
print "Batch:", start, "Run time:", tFinish, "Names:", len(c), "Rate:", len(c)/tFinish.total_seconds()

