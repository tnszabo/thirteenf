# deprecated!
# now merged into fidelity and thirteenfdb
import urllib
from lxml import html, etree
import thirteenfdb as db
import sqlite3

fidelity = "http://quotes.fidelity.com/mmnet/SymLookup.phtml?reqforlookup=REQUESTFORLOOKUP&productid=mmnet&isLoggedIn=mmnet&rows=50&for=stock&by=cusip&criteria={cusiparg}&submit=Search"
cusips = db.getCusips()
conn = db.getDbConn()

for cusip in cusips:
    lookup = fidelity.format(cusiparg=str(cusip))
    page = html.fromstring(urllib.urlopen(lookup).read())
    name = page.xpath('//td/font')[4].text
    symbol = page.xpath('//a')[6]
    print cusip, symbol.text, name
    try:
        conn.execute('''insert into names (CUSIP, Symbol, Name) values(?, ?, ?)''',(cusip, symbol.text, name))
    except: 
        pass
conn.commit()