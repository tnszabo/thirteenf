import lib.thirteenf_mongo as db
import lib.getedgarfiling as ed
import datetime
import pandas as pd
from pymongo import MongoClient

conn = MongoClient()   
flngs = conn.thirteenfdb.filings

# use find to query mongo
# convert result to list
# convert list to dataframe

fl = flngs.find({}, {"cik":1,"manager_name":1, "_id":0}).distinct("manager_name")
print "all current managers:", pd.DataFrame(list(fl))

# select distinct periodofreport
fl = flngs.find({}, {"periodofreport":1, "_id":0}).distinct("periodofreport")
print "all periodofreport:", pd.DataFrame(list(fl))

#print "pivot by period"
fl = flngs.find({}, \
    {"periodofreport":1, "manager_name":1, "cik":1, "nameofissuer":1, \
    "tableentrytotal":1, "tablevaluetotal":1, "_id":0})
c = pd.DataFrame(list(fl))
pivot = pd.pivot_table(c, index = ['manager_name'], columns = ['periodofreport'], values=['tableentrytotal'])
print pivot

fl = flngs.find({"holdings.nameofissuer":"APPLE INC"},
    {"periodofreport":1, 
    "manager_name":1, 
    "val":"$holdings.value", 
    "_id":0})
aapl = pd.DataFrame(list(fl))
#print "APPLE", aapl

# select * 2016q1
fl = flngs.find(
    {"periodofreport":"2016-06-30"}, 
    {"holdings.nameofissuer":1, "_id":0})
q1 = pd.DataFrame(list(fl))
#q1 = q1.sort_values(['manager_name'], ascending=[True])

print "pipeline - names with greatest overlap"
pipeline = [ 
        {"$match":
            { "periodofreport":"2016-06-30"}},\
        {"$unwind":"$holdings"},
        {"$group": 
            { "_id":"$holdings.nameofissuer", 
            "count": {"$sum":1}}},
        {"$sort": { "count": -1}}
    ]
fl = flngs.aggregate(pipeline)
df = pd.DataFrame(list(fl))
#print df.head(10)

print "pipeline - flatten holdings"
pipeline = [ 
        {"$match":
            { "periodofreport":"2016-06-30", "tablevaluetotal":{"$gt":0}} },
        {"$unwind":"$holdings"},
        {"$project": { "_id":0,
            "manager_name":1,
            "name":"$holdings.nameofissuer", 
            "option":"$holdings.putcall",
            "val":"$holdings.value", 
            "Pct_Filing": {"$divide":["$holdings.value","$tablevaluetotal"] }
        }}
    ]
fl = flngs.aggregate(pipeline)
# for row in fl:
#     print row
df = pd.DataFrame(list(fl))

print "Most concentrated positions"
#print df.sort_values(['manager_name', 'Pct_Filing'], ascending=[True,False])

print "Positions greater than 6%"
#print df[df.Pct_Filing > 0.06].sort_values([ 'Pct_Filing'], ascending=[False])