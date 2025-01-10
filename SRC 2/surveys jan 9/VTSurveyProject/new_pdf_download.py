import requests
import datetime
import socket
from urllib.request import urlretrieve
import os
import random
import pandas as pd
from .file_IO_setup import setup_file_system
from .shared import pull_data_from_excel
import ssl

socket.setdefaulttimeout(15)

def check_kill():
    if os.path.exists('kill_threads.txt'):
        return True
    return False

class Request():
    def get_page_html(self):
        r = requests.get(self.full_link)
        return r.text

class Survey(Request):
    #type_to_destination_path = {'alr':,'rch':,'snf':}
    root_path_to_pdf = 'https://dlp.vermont.gov/sites/dlp/files/documents/'
    def __init__(self, pdf_name):
        self.pdf_name = pdf_name
        self.full_link = Survey.root_path_to_pdf + pdf_name
       


class SurveyLinkPage(Request):
    root_url = 'https://dlp.vermont.gov/'
    def __init__(self, link, year, TYPE):
        self.link,self.year,self.TYPE = link,year,TYPE
        self.full_link = SurveyLinkPage.root_url + self.link
        self.html = self.get_page_html()
        self.survey = self.get_survey()
    def __repr__(self):
        return self.link
    def get_survey(self): 
        L = self.html.splitlines()
        for line in L:
            temp_line = line.lower()
            if '<a href="' in line and '.pdf' in temp_line:
                i2 = temp_line.find('.pdf"')
                i2 = i2+4
                temp_link = line[:i2]
                i1 = len(temp_link) - temp_link[::-1].find('/')
                pdf_name = temp_link[i1:i2]
                return Survey(pdf_name)
    def get_link(self):
        return self.survey.full_link  
        
class SurveyListPage(Request):
    root_url = 'https://dlp.vermont.gov/document-categories/'
    type_to_sub_link = {'alr':'alr-survey-statement','snf':'nursing-home-survey-statements','rch':'rch-survey-statements'} 
    def __init__(self,n,TYPE,search):
        self.n = n-1 #page 1, n = 0
        self.TYPE = TYPE
        self.search = search
        self.sub_path = SurveyListPage.type_to_sub_link[TYPE]
        self.full_link = SurveyListPage.root_url + self.sub_path + '?page=%d'%self.n
        self.html = self.get_page_html()
        self.survey_link_pages = self.get_survey_link_pages()
        
    def get_link(s):
        s1 = s.find('/')
        s2 = s.find('" rel=')
        return s[s1+1:s2]
    def get_year(s):
        for elem in s.split('-'):
            if elem.isdigit() and len(elem)==4:
                return elem
    def get_survey_link_pages(self):
        
        result = []
        L = self.html.splitlines()
        for line in L:
            if '<a href="' in line and 'rel="bookmark">' in line:
                link = SurveyListPage.get_link(line)
                year = SurveyListPage.get_year(link)
                search = self.search
                search1,search2 = '-'.join(search.split(' ')),'_'.join(search.split(' '))
                if (year in years) and ((search in link) or (search1 in link) or (search2 in link)):
                    result.append(SurveyLinkPage(link,year,self.TYPE))
        return result
    def all_links(self):
        all_links = []
        for elem in self.survey_link_pages:
            all_links.append(elem.get_link())
        return all_links

def write_file(path,contents):
    f = open(path, "w")
    f.write(contents)
    f.close()
    print(path, 'write success')

def read_file(path):
    f = open(path, "r")
    return f.read()

def load_TYPE_links(TYPE,n, search = None):   
    links = ['%s LINKS'%TYPE]
    links_count = []
    for i in range(1,n+1):
        if check_kill(): return 'STOP'
        print('starting page',i,'of',n)
        p = SurveyListPage(i,TYPE.lower(),search)
        if p == 'STOP':return 'STOP' #IM NOT GOING TO SACRIFICE THAT MUCH SPEED, SO THIS WILL NEVER BE THE CASE
        links.extend(p.all_links())
        write_file('Survey Statements/%s/PageLinks/%s.txt'%(TYPE,i),repr(p.all_links()))
    to_excel(links,TYPE)


def to_excel(L,TYPE):    
    df = pd.DataFrame(L)
    df.to_excel('Survey Statements/%s/current_%s_pdf_links.xlsx'%(TYPE,TYPE))



def download_TYPE_links(TYPE):
    ssl._create_default_https_context = ssl._create_unverified_context
    path = 'Survey Statements/%s/current_%s_pdf_links.xlsx'%(TYPE,TYPE)
    links = pull_data_from_excel(path,(0,))#('%s LINKS'%TYPE,))
    print(links)
    print(len(links),'PDF files to download')
    #input('press enter to continue')
    destination_path = 'Survey Statements/%s/PDF'%TYPE
    failed = []
    existing_files = os.listdir('Survey Statements/%s/PDF'%TYPE)
    i = 0
    for link in links[1:]:
        if check_kill(): return 'STOP'
        link=link[0] #flatten
        pdf_name = link[len(link)-link[::-1].find('/'):]
        if not pdf_name in existing_files:
            try:
                urlretrieve(link,os.path.join(destination_path,pdf_name)) 
            except Exception as e:
                print(e)
                failed.append(link)
        else: 
            print(link,'skipped')
            #input()
        if i%10==0: print(i,'of',len(links),'completed')
        i += 1
    write_file('Survey Statements/%s'%TYPE + '/FailedDownload.txt','\n'.join(failed))

##########################################################################################################
def main_download(query,start_year,ALR,RCH,SNF):
    print('HEREEEEE')
    currentYear = datetime.datetime.now().year
    global years
    if len(start_year)==4:
        start_year = int(start_year)
    else: start_year = 2018
    years = [str(i) for i in range(start_year,currentYear+1)]
    
    files = os.listdir()
    if not ('Survey Statements' in files):
        setup_file_system()
    #query = '-'.join(query.split(' '))
    print(query)
    result = 'go'
    if ALR: 
        result = load_TYPE_links('ALR',10,search = query)#13
    if RCH and result!='STOP': 
        result = load_TYPE_links('RCH',10,search = query)  #47
    if SNF and result!='STOP': 
        result = load_TYPE_links('SNF',10,search = query)#132
    print('downloading links that just loaded')
    if ALR and result!='STOP': 
        result = download_TYPE_links('ALR')
    if RCH and result!='STOP': 
        result = download_TYPE_links('RCH')
    if SNF and result!='STOP': 
        result = download_TYPE_links('SNF')
    print(result)
    print('done or program terminated')
    write_file('download_complete.txt','Testing')
#main()

