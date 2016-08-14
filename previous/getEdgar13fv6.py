import requests
from lxml import etree, html
import pandas as pd

class Cik:
    # Class to take a single CIK code and retrieve the 13F filing
    # Output is a list
    #
    # TODO:
    # add an option for a date range     
    # Edgar Url with key options type=13F-HR, count=1, output=atom
    EDGAR_URL = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_arg}&type=13F-HR&dateb=&owner=exclude&count=1&output=atom"
    NS_INFO_TABLE = "{http://www.sec.gov/edgar/document/thirteenf/informationtable}"
    NS_ATOM = "{http://www.w3.org/2005/Atom}"
    
    
    def __init__(self):            
        # set up info table tags
        self.nameOfIssuer_tag = "".join([self.NS_INFO_TABLE, "nameofissuer"])
        self.titleOfClass_tag = "".join([self.NS_INFO_TABLE, "titleofclass"])
        self.cusip_tag = "".join([self.NS_INFO_TABLE, "cusip"])
        self.value_tag = "".join([self.NS_INFO_TABLE, "value"])      
        shrsOrPrnAmt_tag = "".join([self.NS_INFO_TABLE, "shrsorprnamt/"])
        self.sshPrnamt_tag = "".join([shrsOrPrnAmt_tag, self.NS_INFO_TABLE, "sshprnamt"])
        self.putCall_tag = "".join([self.NS_INFO_TABLE, "putcall"])
        
    def validate(self, cik):
        # Validate given ticker by making a call to EDGAR website with constructed URL.
        url = self.EDGAR_URL.format(cik_arg=cik)
        cik_validation = requests.get(url)
        if not '<?xml' in cik_validation.content[:10]:                        
            return False
        else:
            return True
                
    def process_cik(self, cik):
        # argument: a single CIK number
        # validate the CIK: calls requests.get(url) and tests for <?xml in response
        # get feed: calls etree.parse(edgarUrl) to get atom feed for given CIK
        # get latest filing detail page: calls link.get(href)
        # get latest filing txt file:
        # split file into primary_doc and info_table
        str_cik=cik
        #if not self.validate(str_cik):
	    #     return None
	    # insert CIK into URL
        # This atom feed contains a list of all 13F-HR filings for the given CIK.
        edgarFeed = etree.parse(self.EDGAR_URL.format(cik_arg=str_cik))
        if edgarFeed is None:
            return None
        # get latest filing detail page
        link = edgarFeed.find("".join([self.NS_ATOM,"entry/",self.NS_ATOM,"link"]))
        if link is None:
            return None
        txt_link = link.get("href")  # get first href
        # read html table on page
        latestFiling = pd.io.html.read_html(txt_link)[0]
        # column 2 holds the filenames    
        # construct url to retrieve the reports
        urlsplit = txt_link.split('/')
        edgarbase = '/'.join(urlsplit[:len(urlsplit)-1]) 
        #print edgarbase
        # get column 2 row 5
        # TODO what if text file is not on row 5?
        txt_link = '/'.join([edgarbase,latestFiling[2][5]])
        return self.getFiling(txt_link)
        
    def getFiling(self, txt_link):
        # get the filing as html file      
        # This is not a well formed xml document. 
        filing = html.parse(txt_link)
        cik = filing.findtext("//cik")
        rpt_date = filing.findtext("//periodofreport")
        mgr_name = filing.findtext('//name')
        info_tables = filing.find('//informationtable')
        txt_file_xml = etree.fromstring(html.tostring(info_tables))
        RptInfoTable = []
        # iterate over infotable
        for infoField in txt_file_xml:
            commaList = []
            appnd = commaList.append
            appnd(mgr_name)
            appnd(cik)
            appnd(rpt_date)     
            appnd(infoField.find(self.cusip_tag))
            appnd(infoField.find(self.nameOfIssuer_tag))
            appnd(infoField.find(self.value_tag))
            appnd(infoField.find(self.sshPrnamt_tag))        
            appnd(infoField.find(self.titleOfClass_tag))
            appnd(infoField.find(self.putCall_tag))
            commaSeparated = self.prep_csv_string(commaList)            
            RptInfoTable.append(commaSeparated)
        return RptInfoTable

    def prep_csv_string(self, commaList):       
        # handles cases where input is Null, string or object
        commaSeparated = []
        for x in commaList:
            if x is None:
                commaSeparated.append('')
            elif isinstance(x,str):
                commaSeparated.append(x)
            else:
                commaSeparated.append(x.text)
        return commaSeparated
                    
if __name__ == '__main__':
    # call cik to retrieve and parse 13F filings by CIK code
    ticker=Cik()
    # ticker.process_cik(sys.argv[1])
    # 0001425999
    print ticker.process_cik('0001137521')