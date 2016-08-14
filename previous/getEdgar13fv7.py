import sys
import requests
from lxml import etree, html
import re
import csv 

class Cik:
    # Class to take a single CIK code and retrieve the 13F filing
    # Output is a list
    #
    # TODO:
    # add an option for a date range     

    # Edgar Url with key options type=13F-HR, count=1, output=atom
    EDGAR_URL = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_arg}&type=13F-HR&dateb=&owner=exclude&count=1&output=atom"
    NS_PRI_DOC = "{http://www.sec.gov/edgar/thirteenffiler}"
    NS_INFO_TABLE = "{http://www.sec.gov/edgar/document/thirteenf/informationtable}"
    
    def __init__(self):            
        # init
        # set up primary doc tags
        headerData_tag = "".join([self.NS_PRI_DOC, "headerData/"])
        filerInfo_tag = "".join([self.NS_PRI_DOC, "filerInfo/"])
        formData_tag = "".join([self.NS_PRI_DOC, "formData/"])
        coverPage_tag = "".join([self.NS_PRI_DOC, "coverPage/"])
        summaryPage_tag = "".join([self.NS_PRI_DOC, "summaryPage/"])
        filingManager_tag = "".join([self.NS_PRI_DOC, "filingManager/"])      
        
        self.filingManagerName_tag = "".join([formData_tag, coverPage_tag, filingManager_tag, self.NS_PRI_DOC, "name"])
        self.periodOfReport_tag = "".join([headerData_tag, filerInfo_tag, self.NS_PRI_DOC, "periodOfReport"])
        
        # tableEntryTotal_tag = "".join([formData_tag, summaryPage_tag, self.NS_PRI_DOC, "tableEntryTotal"])
        
        # set up info table tags
        self.infoTable_tag = "".join([self.NS_INFO_TABLE, "infoTable"])
        infoTable_tag2 = self.infoTable_tag + "/"
        self.nameOfIssuer_tag = "".join([self.NS_INFO_TABLE, "nameOfIssuer"])
        self.titleOfClass_tag = "".join([self.NS_INFO_TABLE, "titleOfClass"])
        self.cusip_tag = "".join([self.NS_INFO_TABLE, "cusip"])
        self.value_tag = "".join([self.NS_INFO_TABLE, "value"])      
        shrsOrPrnAmt_tag = "".join([self.NS_INFO_TABLE, "shrsOrPrnAmt/"])
        self.sshPrnamt_tag = "".join([shrsOrPrnAmt_tag, self.NS_INFO_TABLE, "sshPrnamt"])
        self.putCall_tag = "".join([self.NS_INFO_TABLE, "putCall"])
        
    def validate(self, cik):
        # Validate given ticker by making a call to EDGAR website with constructed URL.
        url = self.EDGAR_URL.format(cik_arg=cik)
        cik_validation = requests.get(url)
        if not '<?xml' in cik_validation.content[:10]:                        
            return False
        else:
            return True
                
    def process_cik(self, cik):
        # argument
        str_cik=str(cik)
	    if not self.validate(str_cik):
	        return None
	
        # insert CIK into URL
        edgarUrl = self.EDGAR_URL.format(cik_arg=str_cik)
		
        # The etree.parse() method fetches atom feed from the URL constructed above.
        # This atom feed contains a list of all 13F-HR filings for the given CIK.
        edgarFeed = etree.parse(edgarUrl)
        if edgarFeed is None:
            return None
        
        # Finds index link of the first filing and from that link, constructs the link
        # to the full txt filing and stores it in self.txt_link             
        link = edgarFeed.find("{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}link")
        if link is None:
            return None
            
        link = link.get("href")
        txt_link = ''.join([link[:link.find("-index.htm")], ".txt"])
        
	# get the filing      
        txt_file = requests.get(txt_link).content
        
	# Splits the retrieved txt file into two parts:
        # 1. The primary_doc which contains information about the institution (name,
        #    address etc.)
        # 2. The info_table which contains details regarding number of shares, value etc.
        iter_open_xml = re.finditer(r"<XML>", txt_file)
        iter_close_xml = re.finditer(r"</XML>",txt_file)
        opening_indices = [index.start()+len("<XML>\n") for index in iter_open_xml]
        if len(opening_indices) == 0:
            return None
        closing_indices = [index.start() for index in iter_close_xml]
        primary_doc = txt_file[opening_indices[0]:closing_indices[0]]
        info_table = txt_file[opening_indices[1]:closing_indices[1]]
        primary_doc_parser = etree.fromstring(primary_doc)
        
        
        filing = html.parse(txt_link)
        primary_doc_parser = filing.xpath("//xml")[0]
        # manager name
        mgr_name = primary_doc_parser.find(self.filingManagerName_tag)
        print mgr_name
        # report date for use in file name
        rpt_date = period=primary_doc_parser.find(self.periodOfReport_tag)
        print rpt_date
        # parse the infoTable 
        info_table_parser = etree.fromstring(info_table)                    
        RptInfoTable = []
        
		# iterate over infotable
        for infoField in info_table_parser.findall(self.infoTable_tag):          
            commaList = []
            commaList.append(mgr_name)
            commaList.append(str_cik)
            commaList.append(rpt_date)         
            commaList.append(infoField.find(self.cusip_tag).text)
            commaList.append(infoField.find(self.nameOfIssuer_tag).text)
            commaList.append(infoField.find(self.value_tag).text)
            commaList.append(infoField.find(self.sshPrnamt_tag).text)        
            commaList.append(infoField.find(self.titleOfClass_tag).text)
            commaList.append(infoField.find(self.putCall_tag))
            commaSeparated = self.prep_csv_string(commaList)            
            RptInfoTable.append(commaSeparated)
            
        return RptInfoTable

    def prep_csv_string(self, commaList):       
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
    # 0001079114
    print len(ticker.process_cik('0001569175'))
