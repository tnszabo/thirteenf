import urllib
from lxml import html, etree
import pandas as pd 
from urllib2 import urlopen

# returns a dataframe with new symbols
def getSymbols(cusips):
    FIDELITY_URL = "http://quotes.fidelity.com/mmnet/SymLookup.phtml?reqforlookup=REQUESTFORLOOKUP&productid=mmnet&isLoggedIn=mmnet&rows=50&for=stock&by=cusip&submit=Search"
    names = []
    for cusip in cusips:
        fcusip = cusip.zfill(9)
        p = {'criteria': fcusip}
        url = FIDELITY_URL + "&" + urllib.urlencode(p)
        # print url
        page = urlopen(url).read()
        if "Warning" in page:
            print fcusip, "unknown"
        else:
            df = pd.read_html(page, match="Click symbol for detailed quote", header=1)
            if len(df)==3:
                t = df[2]
                if t['SYMBOL'][0] is not None:
                    s = [cusip, str(t.iloc[0][1]).upper(), t.iloc[0][0]]
                    names.append(s)
                    print s
                    
    dfnames = pd.DataFrame(names, columns=['CUSIP','Symbol','Name'])
    dfnames.set_index('Symbol', inplace=True)
    return dfnames