import lib.thirteenf_sql as db
import pandas as pd

conn = db.getDbConn()

# select distinct cik
print "all current managers"
c = pd.read_sql_query("select distinct cik, manager_name from filings", conn)
print c.sort_values("manager_name")

print "all periods"
c = pd.read_sql_query("select distinct periodofreport from filings", conn)
print c.sort_values("periodofreport")

print "pivot - by period:"
c = pd.read_sql_query("select distinct manager_name, cik, periodofreport, nameofissuer, value, tableentrytotal, tablevaluetotal  from filings", conn)
c = c.sort_values(['periodofreport', 'manager_name', 'value'], ascending=[False,True,False])
pivot = pd.pivot_table(c, index = ['manager_name'], columns = ['periodofreport'], values=['tableentrytotal'])
print pivot

print "q12016"
q1 = pd.read_sql_query("select manager_name, nameofissuer, value, tablevaluetotal from filings \
where periodofreport='2016-06-30'", conn)
q1 = q1.sort_values(['manager_name', 'value'], ascending=[True,False])

print "add pct_filing:" 
q1['Pct_Filing'] = q1.value/q1.tablevaluetotal
#print q1

print "greater than 7%:"
#print q1[q1.Pct_Filing > 0.07]

print "top ten for each mgr"
c['Pct_Filing'] = c.value/c.tablevaluetotal
topten = c.groupby('manager_name').head(10)

print "longevity of top ten"
pivot = pd.pivot_table(topten, index = ['manager_name','nameofissuer'], 
    columns = ['periodofreport'], values = ['Pct_Filing'], margins=True)
#print pivot.groupby(level = [0,1]).mean()

print "most popular names in top ten"
print q1.groupby("nameofissuer").count().sort_values("manager_name", ascending=False).head(10)["manager_name"]

print "pivot - holdings overlap:"
pivot = pd.pivot_table(topten, index = ['nameofissuer'], columns = ['manager_name'], margins=True)
#print pivot