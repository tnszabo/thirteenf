import pandas as pd
import sqlite3 as db

database = '../database/thirteenf_db.sqlite' # name of the sqlite database file
db_flavor = 'sqlite'

# Managers
def getMgrs():
    sqlstmt = 'select distinct cik, manager_name from filings'
    conn = db.connect(database)
    m = pd.read_sql_query(sqlstmt, conn)
    m.set_index(['cik'], drop=False, inplace=True)
    if not m.empty:
        return m['cik'].values.tolist()
    else:
        return None

def getMgrCiks():
    sqlstmt = 'select cik from managers'
    conn = db.connect(database)
    m = pd.read_sql_query(sqlstmt, conn)
    m.set_index(['cik'], drop=False, inplace=True)
    if not m.empty:
        return m['cik'].values.tolist()
    else:
        return None
        
def getNewMgrCiks():
    sqlstmt = 'select cik from managers where cik not in (select distinct cik from filings)'
    conn = db.connect(database)
    m = pd.read_sql_query(sqlstmt, conn)
    if not m.empty:
        return m['cik'].values.tolist()
    else:
        return None

def addMgr(dfMgr):
    conn = db.connect(database)
    dfMgr.to_sql('managers', conn, flavor=db_flavor, if_exists='append', index=True)
    
# Filings
def initFilings(filing):
    conn = db.connect(database)
    filing.to_sql('filings', conn, flavor=db_flavor, if_exists='replace', index=True, index_label=None)
    conn.commit()
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

def getFilingSummary(period):
    conn = db.connect(database)
    sqlstmt = "select distinct cik, manager_name, tableentrytotal \
        from filings where periodofreport = '" +  period + "' order by 2"
    c = pd.read_sql_query(sqlstmt, conn)
    c.set_index(['cik'], inplace=True)
    return c
    
def getMgrSummary(cik):
    conn = db.connect(database)
    sqlstmt = "select distinct cik, manager_name, periodofreport, tableentrytotal \
        from filings where cik = '" +  str(cik) + "' order by 3"
    c = pd.read_sql_query(sqlstmt, conn)
    c.set_index(['periodofreport'], drop=True, inplace=True)
    return c
    
def existsFiling(cik, period):
    conn = db.connect(database)
    sqlstmt = "select count(*) from filings \
        where cik = '"+cik+"' \
        and periodOfReport = '"+period+"'"
    c = conn.execute(sqlstmt)
    r = c.fetchone()
    if r[0] > 0:
        return True
    else:
        return False
    
def getFilings(period):
    conn = db.connect(database)
    sqlstmt = "select cik, cusip, manager_name, periodofreport, \
        nameofissuer, putcall, \
        value, sshprnamt as Shares \
        from filings"
    if period is not None:
        sqlstmt = sqlstmt + " where periodofreport ='" + period + "'"
    c = pd.read_sql_query(sqlstmt, conn)
    m.set_index(['cik','cusip'], drop=True, inplace=True)
    return c
    
# Names
def appendNames(names):    
    conn = db.connect(database)
    names.to_sql('names', conn, flavor=db_flavor, if_exists='append', index=True)
    conn.commit()
    return

# Cusips
def getFilingCusips():
    conn = db.connect(database)
    sqlstmt = 'SELECT distinct cusip from filings order by cusip'
    c = pd.read_sql_query(sqlstmt, conn)
    return c['cusip'].values.tolist()

def getNewCusips():
    conn = db.connect(database)
    sqlstmt = "SELECT distinct cusip from filings where cusip not in " \
        "(select CUSIP from names) order by cusip"
    c = pd.read_sql_query(sqlstmt, conn)
    return c['cusip'].values.tolist()
    
def getDbConn():
    conn = db.connect(database)
    return conn

