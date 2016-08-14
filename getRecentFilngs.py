from lxml import etree
from urllib2 import urlopen
import lib.getedgarfiling as ed
import datetime

class edgarfeed:
    
    def getCiksLinks(self):
        # url for recent 13F filings
        EDGAR_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=13F-HR&count=100&output=atom"
        NS_ATOM = "{http://www.w3.org/2005/Atom}"
        # call Edgar url    
        edgarFeed = etree.parse(urlopen(EDGAR_URL))
        print edgarFeed
        # the feed consists of a list of entries
        entrylist = edgarFeed.findall(NS_ATOM+"entry")
        print entrylist
        links = []
        for entry in entrylist:
            # each entry has a link to the filing details page
            link =  entry.find(NS_ATOM+"link").get("href")
            print link
            # change the link. Select the txt extension. 
            link = ''.join([link[:link.find("-index.htm")], ".txt"])
            links.append(link)
        return links
        
if __name__ == '__main__':
    start = datetime.datetime.now()
    # call cik to retrieve feed
    filings=edgarfeed()
    #mgr=edgarfilings()
    # iterate throught the feed
    for link in filings.getCiksLinks():
        # get each 13f link
        f = ed._get_filing_as_list(link)
        # print filing as a 2D array
        if len(f) > 1:
            print f[1][2],  f[1][0],  len(f)
    print "Run time:", datetime.datetime.now() - start
    

