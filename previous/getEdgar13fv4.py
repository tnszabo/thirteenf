import sys
import requests
from lxml import etree
from urllib2 import urlopen
import re
import csv 

class Cik:
    # Class to take a list of SEC CIK codes and retrieve the 13F filings for each
    # Output is a single csv file with filings for each manager in the input list.
    #
    # TODO:
    # add an option for a date range     
    mgr_name=""    
    rpt_date=""
    txt_link = ""
    primary_doc = ""
    info_table = ""
    cik_counter = 0
    # Edgar Url with key options type=13F-HR, count=1, output=atom
    EDGAR_URL = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_arg}&type=13F-HR&dateb=&owner=exclude&count=1&output=atom"
    NS_PRI_DOC = "{http://www.sec.gov/edgar/thirteenffiler}"
    NS_INFO_TABLE = "{http://www.sec.gov/edgar/document/thirteenf/informationtable}"
    
    def __init__(self, ciks):            
        # argument
        if isinstance(ciks,str):
            self.cik=ciks.split()
        else:
            self.cik = ciks 
                
    def validate(self, cik):
            # Validate given ticker by making a call to EDGAR website with constructed URL.
            url = self.EDGAR_URL.format(cik_arg=cik)
            cik_validation = requests.get(url)
            if not '<?xml' in cik_validation.content[:10]:                        
                    return False
            else:
                    return True
                
    def process_cik_list(self):
        
        # set up primary doc tags
        headerData_tag = "".join([self.NS_PRI_DOC, "headerData/"])
        filerInfo_tag = "".join([self.NS_PRI_DOC, "filerInfo/"])
        formData_tag = "".join([self.NS_PRI_DOC, "formData/"])        
        coverPage_tag = "".join([self.NS_PRI_DOC, "coverPage/"])
        summaryPage_tag = "".join([self.NS_PRI_DOC, "summaryPage/"])
        filingManager_tag = "".join([self.NS_PRI_DOC, "filingManager/"])      
        filingManagerName_tag = "".join([formData_tag, coverPage_tag, filingManager_tag, self.NS_PRI_DOC, "name"])
        periodOfReport_tag = "".join([headerData_tag, filerInfo_tag, self.NS_PRI_DOC, "periodOfReport"])
        tableEntryTotal_tag = "".join([formData_tag, summaryPage_tag, self.NS_PRI_DOC, "tableEntryTotal"])
        # set up info table tags
        infoTable_tag = "".join([self.NS_INFO_TABLE, "infoTable"])
        infoTable_tag2 = infoTable_tag + "/"
        nameOfIssuer_tag = "".join([self.NS_INFO_TABLE, "nameOfIssuer"])
        titleOfClass_tag = "".join([self.NS_INFO_TABLE, "titleOfClass"])
        cusip_tag = "".join([self.NS_INFO_TABLE, "cusip"])
        value_tag = "".join([self.NS_INFO_TABLE, "value"])       
        shrsOrPrnAmt_tag = "".join([self.NS_INFO_TABLE, "shrsOrPrnAmt/"])
        sshPrnamt_tag = "".join([shrsOrPrnAmt_tag, self.NS_INFO_TABLE, "sshPrnamt"])
        putCall_tag = "".join([self.NS_INFO_TABLE, "putCall"])
            
        for cik in self.cik:
            str_cik = cik[0]            
            if not self.validate(str_cik):
               print "Invalid CIK - "+str_cik
               continue
                   
            # insert CIK into URL
            edgarUrl = self.EDGAR_URL.format(cik_arg=str_cik)
            # The etree.parse() method fetches atom feed from the URL constructed above.
            # This atom feed contains a list of all 13F-HR filings for the given CIK.
            self.edgarFeed = etree.parse(urlopen(edgarUrl))
            # Finds index link of the first filing and from that link, constructs the link
            # to the full txt submission and stores it in self.txt_link             
            link = self.edgarFeed.find("{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}link").get("href")
            self.txt_link = ''.join([link[:link.find("-index.htm")], ".txt"])
            # Splits the retrieved txt file into two parts:
            # 1. The primary_doc which contains information about the institution (name,
            #    address etc.)
            # 2. The info_table which contains details regarding number of shares, value etc.
            #get the txt_link file      
            txt_file = requests.get(self.txt_link).content
            iter_open_xml = re.finditer(r"<XML>", txt_file)
            iter_close_xml = re.finditer(r"</XML>",txt_file)        
            opening_indices = [index.start()+len("<XML>\n") for index in iter_open_xml]
            closing_indices = [index.start() for index in iter_close_xml]
            self.primary_doc = txt_file[opening_indices[0]:closing_indices[0]]
            self.info_table = txt_file[opening_indices[1]:closing_indices[1]]
            
            primary_doc_parser = etree.fromstring(self.primary_doc)               
            # get manager name
            self.mgr_name = primary_doc_parser.find(filingManagerName_tag).text
            # get report date for use in file name
            self.rpt_date = period=primary_doc_parser.find(periodOfReport_tag)
            out_file = "./output/13F_"+self.rpt_date.text+".txt"
            
            # once per execution, but after the first cik
            if self.cik_counter == 0:            
                writer = csv.writer(open(out_file,"wb"), dialect='excel', quoting=csv.QUOTE_ALL)        
                header = []
                header.append("Manager")
                header.append("MgrCik")
                header.append("Period")             
                header.append("CUSIP")
                header.append("Name")
                header.append("Value")
                header.append("Shares")
                header.append("Class")
                header.append("PutCall")
                writer.writerow(header)
                
            self.cik_counter += 1
            print " - ".join([str(self.cik_counter), self.mgr_name, self.rpt_date.text, primary_doc_parser.find(tableEntryTotal_tag).text])

            # write out the results
            writer = csv.writer(open(out_file,"ab"), dialect='excel', quoting=csv.QUOTE_ALL)

            # get all the information in each infoTable tag
            info_table_parser = etree.fromstring(self.info_table)                    
            for info_table in info_table_parser.findall(infoTable_tag):          
                commaList = []
                commaList.append(self.mgr_name)
                commaList.append(str_cik)
                commaList.append(self.rpt_date)         
                commaList.append(info_table.find(cusip_tag))
                commaList.append(info_table.find(nameOfIssuer_tag))
                commaList.append(info_table.find(value_tag))
                commaList.append(info_table.find(sshPrnamt_tag))        
                commaList.append(info_table.find(titleOfClass_tag))
                commaList.append(info_table.find(putCall_tag))
                commaSeparated = self.prep_csv_string(commaList)            
                writer.writerow(commaSeparated)


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
    ticker=Cik('0001425999')
    ticker.process_cik_list()

