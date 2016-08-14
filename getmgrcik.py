import lib.getedgarfiling as ed
import datetime

start =  datetime.datetime.now()

result = ed.get_cik('Whale Rock')    
if result:
    print result

print datetime.datetime.now() - start