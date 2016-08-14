import pandas as pd
# define target database
from pymongo import MongoClient
database = '../database/thirteenf_db.sqlite' # name of the sqlite database file
db_flavor = 'sqlite'

def getMgrCiks():
    connection = MongoClient()    
    mgrs = connection.thirteenfdb.managers
    m = mgrs.find({}, {"_id":0})
    return m

def getFilingCiks():
    connection = MongoClient()    
    flngs = connection.thirteenfdb.filings
    f = flngs.find({}, {"_id":0, "cik":1})
    return f

#def delFilings():
    #c.execute('delete from filings')

def insertFiling(filing):
    connection = MongoClient()    
    flngs = connection.thirteenfdb.filings
    flngs.insert(filing)
    return

def appendFilings(filing):
    conn = db.connect(database)
    try:
        filing.to_sql('filings', conn, flavor=db_flavor, if_exists='append', index=True, index_label=None)
    except Exception as err:
        print err
        pass
    conn.commit()
    return

def appendNames(names):    
    conn = db.connect(database)
    names.to_sql('names', conn, flavor=db_flavor, if_exists='append', index=True, index_label=None)
    conn.commit()
    return

def getFilingCusips():
    conn = db.connect(database)
    sqlstmt = 'SELECT distinct cusip from filings where PutCall="" order by name'
    c = pd.read_sql_query(sqlstmt, conn)
    return c['cusip'].values.tolist()

def getNewCusips():
    conn = db.connect(database)
    sqlstmt = "SELECT distinct cusip from filings where cusip not in " \
    "(select CUSIP from names order by CUSIP) order by cusip"
    c = pd.read_sql_query(sqlstmt, conn)
    return c['cusip'].values.tolist()
    
def getDbConn():
    conn = db.connect(database)
    return conn

def getFilingCount(manager):
    conn = db.connect(database)
    sqlstmt = "select manager, periodOfReport, count(*) \
    from filings where MgrCik = '"+manager+"' group by manager, periodOfReport" 
    #c = conn.cursor()
    c = conn.execute(sqlstmt)
    print c.rowcount
    #c = pd.read_sql_query(sqlstmt, conn)
    return True
    
def existsFiling(manager, period):
    connection = MongoClient()    
    flngs = connection.thirteenfdb.filings
    f = flngs.find({"cik":manager, "periodofreport":period}, {"_id":0})
    if f.alive:
        return True
    return False
    if f.size()>0:
def getFilings():
    conn = db.connect(database)
    sqlstmt = "select manager, '13F' as Source, Period, 'Holding' as Record_Type, 'L' as LS, \
    CASE WHEN PutCall>'' THEN PutCall ELSE Class END as Asset_Class, \
    Value, Shares, Pct_Filing*100 as Long_Percent, \
    CASE WHEN n.Symbol is null THEN f.CUSIP ELSE n.Symbol END as Symbol, \
    CASE WHEN n.Name>'' THEN n.Name ELSE f.Name END as Name, \
    manager as ManagerFirm \
    from filings f left outer join names n on n.cusip=f.cusip"
    c = pd.read_sql_query(sqlstmt, conn)
    return c
    
def createTableFilings(): 
    conn = db.connect(database)
    c = conn.cursor()
    c.execute("drop table filings")
    c.execute('CREATE TABLE filings \
        (    Period DATE NOT NULL,\
        MANAGER VARCHAR(64) NOT NULL,\
        MgrCik VARCHAR(10) NOT NULL,\
        CUSIP VARCHAR(9) NOT NULL, \
        Name VARCHAR(64),\
        Class VARCHAR(8),\
        PutCall VARCHAR(8),\
        Value DECIMAL(10,2) NOT NULL,\
        Shares INTEGER NOT NULL,\
        Pct_Filing DECIMAL(10,2),\
        PRIMARY KEY (MANAGER, MgrCik, Period, CUSIP, Class, PutCall))')
    conn.commit()

# deprecated
def createTableTempfilings(): 
    conn = db.connect(database)
    c = conn.cursor()
    c.execute('CREATE TABLE tempfilings \
        (    Period DATE NOT NULL,\
        MANAGER VARCHAR(64) NOT NULL,\
        MgrCik VARCHAR(10) NOT NULL,\
        CUSIP VARCHAR(9) NOT NULL, \
        Name VARCHAR(64),\
        Class VARCHAR(8),\
        PutCall VARCHAR(8),\
        Value DECIMAL(10,2) NOT NULL,\
        Shares INTEGER NOT NULL,\
        Pct_Filing DECIMAL(10,2),\
        PRIMARY KEY (MANAGER, MgrCik, Period, CUSIP, Class, PutCall))')
    conn.commit()