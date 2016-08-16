import requests
from lxml import etree, html
from xml.etree.ElementTree import ParseError
from urllib2 import urlopen
from urllib import urlencode
import json
import pandas as pd
import numpy as np
import csv
import datetime
import time

# getedgarfilnig module to connect to SEC Edgar system 
# Extracts CIK codes
# Looks up URL for manager atom feeds
# gets filings
# 13F filings are in hybrid html and xml format
# we use html parsing, iter, xpath and find

# Edgar Url with necessary options type=13F-HR, count=1, output=atom
EDGAR_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_arg}&type=13F-HR&output=atom"
ATOM_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=13F-HR&output=atom"
NS_INFO_TABLE = "{http://www.sec.gov/edgar/document/thirteenf/informationtable}"
NS_ATOM = "{http://www.w3.org/2005/Atom}"
EDGAR_BASE = 'https://www.sec.gov/Archives/edgar/data'
ATOM_PATH = "".join([NS_ATOM,"entry/",NS_ATOM,"content/",NS_ATOM, "accession-nunber"])

def get_cik(manager):
    LOOKUP_URL = "https://www.sec.gov/cgi-bin/browse-edgar?owner=exclude&action=getcompany"
    p = {'company': manager}
    url = LOOKUP_URL + '&' +urlencode(p)
    try:
        df = pd.read_html(url, header=0, index_col=0)
        return df
    except Exception as err: 
        print "get_cik:", err
        return False
    
def get_urls_available(cik):
    # argument: a single CIK number
    # This atom feed contains a list of all 13F-HR filings for the given CIK.
    p = {'CIK':str(cik).zfill(10)}
    url = ATOM_URL + "&" + urlencode(p)
    try:
        atomPage = etree.parse(urlopen(url))
    except Exception as err:
        print "get_urls_available:", err
        return None
    availFilings = {}
    for e in atomPage.iter(NS_ATOM+"content"):
        accNum = e.find("{http://www.w3.org/2005/Atom}accession-nunber").text
        date = e.find("{http://www.w3.org/2005/Atom}filing-date").text
        pfdate = date.split('-')
        dpfdate = datetime.date(int(pfdate[0]), int(pfdate[1]), int(pfdate[2]))
        lastPeriod = previous_quarter(dpfdate)
        availFilings[lastPeriod] = "/".join([EDGAR_BASE, cik, accNum.replace("-",""), accNum])+'.txt'
    df1 = pd.DataFrame(availFilings, index=availFilings.keys()).sort_index(level=0)
    return df1
    
def get_url_fordate(cik, period):
    alldates = get_urls_available(cik)
    return alldates[period]
    
def get_url(cik):
    # argument: a single CIK number
    # This atom feed contains a list of all 13F-HR filings for the given CIK.
    mycik = str(cik).zfill(10)
    filingUrl = None
    try:
        p = {'CIK': mycik}
        url = ATOM_URL + "&" + urlencode(p)
        atomPage = etree.parse(urlopen(url))
    except Exception as err:
        print "get_url:", err
        atomPage = None
        return False
    if atomPage is not None:
        #find accession number of most recent filing entry
        accNum = atomPage.findtext(ATOM_PATH)
        filingUrl = "/".join([EDGAR_BASE, mycik, accNum.replace("-",""), accNum])+'.txt'
    return filingUrl

def _get_xml(url):
    try:
        stream = urlopen(url)
        return html.parse(stream)
    except Exception as e:
        print e
        return None
    
def _xml_tojson(filing):   
    #print filing
    #filing = html.cleaner(Comment=False, Structure=False)
    json = None
    if filing is not None:
        oMgrFiling = {}
        # new implementation that uses xpath and iter 
        snippet = filing.xpath('//xml/edgarsubmission/formdata', namespace='http://www.sec.gov/edgar/thirteenffiler')
        if not snippet==[]:
            snippet=snippet[0]
            for child in snippet.iter():
                if not len(child):
                    if child.text.isdigit():
                        oMgrFiling[child.tag] = int(child.text)
                    else:
                        oMgrFiling[child.tag] = child.text
    
            snippet = filing.xpath('//xml/edgarsubmission/headerdata', namespace='http://www.sec.gov/edgar/thirteenffiler')[0]
            for child in snippet.iter():
                if not len(child):
                    if child.text.isdigit():
                        oMgrFiling[child.tag] = int(child.text)
                    else:
                        oMgrFiling[child.tag] = child.text
    
            oHoldings = [] 
            for holding in filing.xpath('//xml/informationtable', namespace=NS_INFO_TABLE)[0]: 
                oHolding = {}
                for field in holding.iter():
                    if field.text is None:
                        continue
                    if field.text.isdigit():
                        oHolding[field.tag] = int(field.text)
                    else:
                        oHolding[field.tag] = field.text
                oHolding['cusip'] = str(holding.findtext('cusip'))
                oHoldings.append(oHolding) #holdings as array
            oMgrFiling['holdings']=oHoldings
            json = oMgrFiling
            
            # override key fields
            json['manager_name'] = filing.findtext('//name') #add new tag for manager name
            # reformat date
            period = filing.findtext('//periodofreport')
            p = period.split('-')
            json['periodofreport'] = '-'.join([p[2],p[0],p[1]])
            json['cik'] = str(filing.findtext('//cik'))
            # quick fixes for rarley seen fields which are not in filing schema
            # oFiling.pop('amendmentno',None)
    return json

def _json_togoogjson(json):
    # convert to df
    # flatten df
    # convery to goog json
    goog = {}
    cols = []
    for col in json.keys():
        cols.append({"label":col,"type":type(col)})
    goog['cols'] = cols
    rows = []
    for row in json:
        rows.append({"c":row.value})
    goog['rows'] = rows
    return goog
    
def _json_todf(json):
    df = pd.read_json(json.dumps(json))
    return df
    
def _get_filing_as_list(url):
    print "_get_filing_as_list is deprecated"
    filing = _get_xml(url)
    filings = None
    if filing is not None:
        cik = filing.findtext('//cik')
        rpt_date = filing.findtext("//periodofreport")
        mgr_name = filing.findtext('//name')
        info_tables = filing.find( '//informationtable')
        # create header row
        filings = [["Manager_name","Cik","Period","CUSIP","Name","Class","PutCall","Value","Shares"]]
        for entry in info_tables:
            rawHolding = []
            a = rawHolding.append
            a(mgr_name)
            a(cik)
            a(rpt_date)     
            ft = entry.findtext
            a(ft('cusip'))
            a(ft('nameofissuer'))
            a(ft('titleofclass'))
            a(ifnull(entry.find('putcall'),''))
            a(int(ft('value')))
            a(int(ft('.//sshprnamt')))      
            filings.append(rawHolding)
    return filings

def get_filing_as_json(cik):
    return _xml_tojson(_get_xml(get_url(cik)))

def get_filing_as_df(cik):
    return _json_todf(get_filing_as_json(cik))

# def _get_filing_as_df(url):
#     if url is not None:
#         filing = _get_filing_as_list(url)
#         df = pd.DataFrame(filing[1:], columns=filing[0])
#         grouped = pd.pivot_table(df, index = ['Period','Manager', 'MgrCik',  'CUSIP', 'Name', 'Class', 'PutCall'] , aggfunc=np.sum)
#         grouped['Pct_Filing'] = grouped['Value'].groupby(level = 2).transform(lambda x: x/x.sum())
#     return grouped
    
def ifnull(element, s):
    return s if element is None else element.text

def previous_quarter(ref):
    if ref.month < 4:
        prev = datetime.date(ref.year - 1, 12, 31)
    elif ref.month < 7:
        prev = datetime.date(ref.year, 3, 31)
    elif ref.month < 10:
        prev = datetime.date(ref.year, 6, 30)
    else:
        prev = datetime.date(ref.year, 9, 30)
    return prev.strftime('%Y-%m-%d')