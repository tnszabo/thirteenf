import pandas as pd
# define target database
from pymongo import MongoClient

def getMgrCiks():
    connection = MongoClient()    
    mgrs = connection.thirteenfdb.managers
    ciks = mgrs.distinct("cik")
    # m = mgrs.find({}, {"_id":0, "cik":1})
    # ciks = []
    # for mgr in m:
    #     ciks.append(str(mgr['cik']).zfill(10))
    return ciks

def getFilingCiks():
    connection = MongoClient()    
    flngs = connection.thirteenfdb.filings
    ciks = flngs.distinct("cik")
    # f = flngs.find({}, {"_id":0, "cik":1})
    # ciks = []
    # for mgr in f:
    #     ciks.append(str(mgr['cik']).zfill(10))
    # print ciks
    return ciks

def insertMgrsFromFilings():
    connection = MongoClient()    
    dbf = connection.thirteenfdb.filings
    dbm = connection.thirteenfdb.managers
    mgrs = dbf.distinct("cik")
    for m in mgrs:
        doc = {"cik": m}
        dbm.insert(doc)
        
def insertFiling(filing):
    connection = MongoClient()    
    flngs = connection.thirteenfdb.filings
    try:
        flngs.insert(filing)
    except Exception as e:
        print e
        pass
    return

def appendFilings(filing):
    connection = MongoClient()    
    flngs = connection.thirteenfdb.filings
    try:
        flngs.insert(filing)
    except Exception as e:
        print e
        pass
    return

def getDbConn():
    conn = MongoClient()    
    return conn.thirteenfdb

def existsFiling(cik, period):
    connection = MongoClient()    
    flngs = connection.thirteenfdb.filings
    flngs.find()
    f = flngs.find({"cik":str(cik).zfill(10), "periodofreport":period}).limit(1)
    if len(list(f))>0:
        return True
    else:
        return False
        
def getFilings(qry):
    connection = MongoClient()    
    flngs = connection.thirteenfdb.filings
    f = flngs.find(qry, {"manager_name":1, "periodofreport":1, "tableentrytotal":1, "tablevaluetotal":1, "_id":0})
    #.sort({"manager_name":1, "periodofreport":1})
    return pd.DataFrame(list(f))