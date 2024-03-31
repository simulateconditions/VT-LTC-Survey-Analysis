import requests
import datetime
import socket
from urllib.request import urlretrieve
import os
import random
import pandas as pd
socket.setdefaulttimeout(15)
currentYear = datetime.datetime.now().year
years = [str(i) for i in range(2018,currentYear+1)]


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
    def __init__(self,n,TYPE):
        self.n = n-1 #page 1, n = 0
        self.TYPE = TYPE
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
                if year in years: 
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

def load_TYPE_links(TYPE,n):   
    links = ['%s LINKS'%TYPE]
    for i in range(1,n+1):
        print('starting page',i,'of',n)
        p = SurveyListPage(i,TYPE.lower())
        links.extend(p.all_links())
    to_excel(links,TYPE)

def to_excel(L,TYPE):    
    df = pd.DataFrame(L)
    df.to_excel('current_%s_pdf_links.xlsx'%TYPE)

def pull_data_from_excel(p,columns_to_pull):
    #p = 'InventoryValuation.xlsx'
    data = pd.read_excel(p) 
    df = pd.DataFrame(data, columns=columns_to_pull)
    L = df.values.tolist() #this is a list of itemId matched with BBVT Warehouse (Value)
    return L

def download_TYPE_links(TYPE):
    path = 'current_%s_pdf_links.xlsx'%TYPE
    links = pull_data_from_excel(path,('%s LINKS'%TYPE,))
    print(len(links),'PDF files to download')
    input('press enter to continue')
    destination_path = 'Documents/Survey Statements/%s/PDF'%TYPE
    failed = []
    existing_files = os.listdir('Documents/Survey Statements/%s/PDF'%TYPE)
    i = 0
    for link in links:
        link=link[0] #flatten
        pdf_name = link[len(link)-link[::-1].find('/'):]
        if not pdf_name in existing_files:
            try:
                urlretrieve(link,os.path.join(destination_path,pdf_name)) 
            except:
                failed.append(link)
        else: 
            print(link,'skipped')
            input()
        if i%10==0: print(i,'of',len(links),'completed')
        i += 1
    write_file(destination_path + '/Failed.txt',failed)

##########################################################################################################
def main():
    #load_TYPE_links('ALR',13)
    #load_TYPE_links('RCH',42)    
    #load_TYPE_links('SNF',132)
    #x = input('press enter to download links that just loaded')
    download_TYPE_links('ALR')
    download_TYPE_links('RCH')
    download_TYPE_links('SNF')

main()

