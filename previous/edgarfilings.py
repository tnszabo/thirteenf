import requests
from lxml import etree, html
import pandas as pd
import numpy as np
#import sqlite3

class edgarfilings:
    # Class to take a single CIK code and retrieve the 13F filing
    # TODO:
    # add an option for a date range     
    
    # Edgar Url with necessary options type=13F-HR, count=1, output=atom
    EDGAR_URL = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_arg}&type=13F-HR&dateb=&owner=exclude&count=1&output=atom"
    
    def __init__(self):            
        # set up info table tags
        NS_INFO_TABLE = "{http://www.sec.gov/edgar/document/thirteenf/informationtable}"
        self.nameOfIssuer_tag = "".join([NS_INFO_TABLE, "nameofissuer"])
        self.titleOfClass_tag = "".join([NS_INFO_TABLE, "titleofclass"])
        self.cusip_tag = "".join([NS_INFO_TABLE, "cusip"])
        self.value_tag = "".join([NS_INFO_TABLE, "value"])      
        shrsOrPrnAmt_tag = "".join([NS_INFO_TABLE, "shrsorprnamt/"])
        self.sshPrnamt_tag = "".join([shrsOrPrnAmt_tag, NS_INFO_TABLE, "sshprnamt"])
        self.putCall_tag = "".join([NS_INFO_TABLE, "putcall"])

    def get_filing_as_list(self, cik):
        return self._get_filing_as_list(self.get_filings_url(cik))

    def get_filing_as_df(self, cik):
        return self._get_filing_as_df(self.get_filings_url(cik))

    def get_filings_url(self, cik):
        NS_ATOM = "{http://www.w3.org/2005/Atom}"
        # argument: a single CIK number
        # This atom feed contains a list of all 13F-HR filings for the given CIK.
        print self.EDGAR_URL.format(cik_arg=cik)
        filingPage = etree.parse(self.EDGAR_URL.format(cik_arg=cik))
        print filingPage
        filingUrl=""
        if filingPage is not None:
            link = filingPage.find("".join([NS_ATOM,"entry/",NS_ATOM,"link"]))
            # TODO: what if top entry is not the desired date? 
            if link is not None:
                filingUrl = link.get("href")  # get first href
                print link.get("entry/content/filing-date")
                print filingUrl
                # read html table on page
                latestFiling = pd.io.html.read_html(filingUrl)[0]
                # construct url to retrieve the reports
                urlsplit = filingUrl.split('/')
                edgarbase = '/'.join(urlsplit[:len(urlsplit)-1])
                # get column 2 row 5
                filingUrl = '/'.join([edgarbase,latestFiling[2][5]])
        return filingUrl
            
    def _get_filing_as_df(self, url):
        filing = self._get_filing_as_list(url)
        df = pd.DataFrame(filing[1:], columns=filing[0])
        #print df.size
        grouped = pd.pivot_table(df, index = ['Period','Manager', 'MgrCik',  'CUSIP', 'Name', 'Class', 'PutCall'] , aggfunc=np.sum)
        #print grouped.size
        return grouped
        
    def _get_filing_as_list(self, url):
        # get the filing as html file      
        # This is not a well formed xml document. 
        filing = html.parse(url)
        cik = filing.findtext("//cik")
        rpt_date = filing.findtext("//periodofreport")
        mgr_name = filing.findtext('//name')
        info_tables = filing.find('//informationtable')
        xmlFiling = etree.fromstring(html.tostring(info_tables))
        # create header row
        filing = [["Manager","MgrCik","Period","CUSIP","Name","Class","PutCall","Value","Shares"]]
        # iterate over xml filing
        for entry in xmlFiling:
            if entry.find(self.cusip_tag) is not None: 
                rawHolding = []
                a = rawHolding.append
                a(mgr_name)
                a(cik)
                a(rpt_date)     
                f = entry.find
                a(f(self.cusip_tag).text)
                a(f(self.nameOfIssuer_tag).text)
                a(f(self.titleOfClass_tag).text)
                a(self.naifnull(f(self.putCall_tag)))
                a(int(f(self.value_tag).text))
                a(int(f(self.sshPrnamt_tag).text))        
                filing.append(rawHolding)
        return filing
    
    def validate_cik(self, cik):
        # Validate given ticker by making a call to EDGAR website with constructed URL.
        url = self.EDGAR_URL.format(cik_arg=cik)
        cik_validation = requests.get(url)
        if not '<?xml' in cik_validation.content[:10]:                        
            return False
        else:
            return True
            
    def naifnull(self, element):
        return 'COM' if element is None else element.text
        
if __name__ == '__main__':
    # call cik to retrieve and parse 13F filings by CIK code
    # hf.process_cik(sys.argv[1])
    hf=edgarfilings()
    result = hf.get_filing_as_df('0001575766')
    #print result
    
   
    #print hf.get_filing_as_list('0001137521')