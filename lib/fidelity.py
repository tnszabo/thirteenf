import urllib
import pandas as pd 


def getSymbols(cusips):
    FIDELITY_URL = "http://quotes.fidelity.com/mmnet/SymLookup.phtml?reqforlookup=REQUESTFORLOOKUP&productid=mmnet&isLoggedIn=mmnet&rows=50&for=stock&by=cusip&submit=Search"
    names = []
    for cusip in cusips:
        cusip = cusip.zfill(9)
        p = {'criteria': cusip}
        url = FIDELITY_URL + "&" + urllib.urlencode(p)
        df = pd.read_html(url,   match="Click symbol for detailed quote", header=0)
        if len(df)==3:
            t = df[2]
            name = [cusip, t.loc[1][1], t.loc[1][0]]
            print name
            names.append(name)
    # add column names    
    dfnames = pd.DataFrame(names, columns=['CUSIP','Symbol','Name'])
    # set cusip as index
    dfnames.set_index('CUSIP', inplace=True)
    return dfnames