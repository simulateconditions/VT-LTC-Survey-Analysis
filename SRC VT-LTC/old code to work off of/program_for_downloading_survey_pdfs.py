import requests
import datetime
import socket
from urllib.request import urlretrieve
import os
socket.setdefaulttimeout(15)
# Step 1
currentYear = datetime.datetime.now().year
years = [str(i) for i in range(2018,currentYear+1)]
print(years)
#read all page=%d until fail - use try except instead of hardcoding # of pages


url_root_1 = 'https://dlp.vermont.gov/document-categories/'
alr_path = 'alr-survey-statement'  #16
snf_path='nursing-home-survey-statements' #197
rch_path = 'rch-survey-statements' #72
#^referred to as category_root

root_path_to_survey_page = 'https://dlp.vermont.gov/'
root_path_to_pdf = 'https://dlp.vermont.gov/sites/dlp/files/documents/'

path_to = input('if the target direcory is not Documents/Survey Statements... please enter the target directory now, else just enter')
if path_to !='': target_directory = path_to
target_directory = 'Documents/Survey Statements/'
print('Target Directory:', target_directory)

'''
Step 1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
create list of page links with ?page=%d
'''


def create_links_to_list_pages(category_root,n):
    A = [category_root]
    for i in range(1,n):
        new_link = category_root+'?page=%d' %i
        A.append(new_link)
    return A

'''
get link list for all 3 categories 
'''

def get_links_to_list_pages(ALR=False,RCH=False,SNF=False):
    alr_links,rch_links,snf_links = [],[],[]
    if ALR:
        alr_n = int(input('How many pages from '+url_root_1+alr_path+' would you like to search? eg.16\n'))
        alr_links = create_links_to_list_pages(alr_path,alr_n)
        print('ALR Links Ready')
        
    if RCH:    
        rch_n = int(input('How many pages from '+url_root_1+rch_path+' would you like to search? eg.72\n'))
        rch_links = create_links_to_list_pages(rch_path,rch_n)
        print('RCH Links Ready')
        
    if SNF:    
        snf_n = int(input('How many pages from '+url_root_1+snf_path+' would you like to search? eg.197\n'))
        snf_links = create_links_to_list_pages(snf_path,snf_n)
        print('SNF Links Ready')
    return alr_links,rch_links,snf_links

    
'''
Step 2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
get urls from these list pages and store
'''
def get_link(s):
    s1 = s.find('/')
    s2 = s.find('" rel=')
    return s[s1:s2]

def get_year(c):
    for elem in c.split('-'):
        if elem.isdigit() and len(elem)==4:
            return elem

def pull_survey_links_from_list_pages(list_page_url):
    survey_links = []
    for sub_path in list_page_url:
        r = requests.get(url_root_1+sub_path)
        c = r.text
        L = c.splitlines()
        for line in L:
            if '<a href="' in line and 'rel="bookmark">' in line:
                survey_link = get_link(line)
                year = get_year(survey_link)
                if year in years:
                    survey_links.append(survey_link)
    return survey_links

def list_files(path_to):
    files_in = os.listdir(path_to)
    return files_in


def download_pdfs(category_name,links):
    this_target_directory = os.path.join(target_directory[:-1],category_name)
    files_already = list_files(this_target_directory)
    failed = ['failed!']
    for link in links:
        new_url = root_path_to_survey_page[:-1] + link
        r = requests.get(new_url)
        text = r.text
        L = text.splitlines()
        found = False
        for line in L:
            if '<a href="' in line and '.pdf' in line:
                found = True
                i2 = line.find('.pdf"')
                i2 = i2+4
                new_link = line[:i2]
                i1 = len(new_link) - new_link[::-1].find('/')
                pdf_name = new_link[i1:i2]
                if not pdf_name in files_already:
                    url_to_pdf = root_path_to_pdf + pdf_name
                    try:
                        urlretrieve(url_to_pdf,os.path.join(this_target_directory,pdf_name)) 
                    except:
                        failed.append(pdf_name)
        if found == False:
            failed.append(pdf_name)
            
            
    f = open(os.path.join(this_target_directory,'failed.txt'), "a")
    f.write(repr(failed))
    f.close()


def dispatch():
    ALR_bool,RCH_bool,SNF_bool = bool(int(input('enter 1 to pull ALR else 0\n'))),bool(int(input('enter 1 to pull RCH else 0\n'))),bool(int(input('enter 1 to pull SNF else 0\n')))
    alr_page_links,rch_page_links,snf_page_links = get_links_to_list_pages(ALR=ALR_bool,RCH=RCH_bool,SNF=SNF_bool)
    print('\nPulling Requested Survey Links from 2018 to Present')
    ALR_survey_links = pull_survey_links_from_list_pages(alr_page_links)
    print(len(ALR_survey_links),'ALR links found...Beginning RCH')
    RCH_survey_links = pull_survey_links_from_list_pages(rch_page_links)
    print(len(RCH_survey_links),'RCH links found...Beginning SNF')
    SNF_survey_links = pull_survey_links_from_list_pages(snf_page_links)
    print(len(SNF_survey_links),'SNF links found.')
    

    print('\nPDF Downloading ...')
    print('\nStarting ALR Downloads Now')
    download_pdfs('ALR/PDF', ALR_survey_links)
    print('ALR Complete...Starting RCH Downloads')
    download_pdfs('RCH/PDF', RCH_survey_links)
    print('RCH Complete...Starting SNF Downloads')
    download_pdfs('SNF/PDF', SNF_survey_links)
    print('SNF Complete')
dispatch()
'''
Step 3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
get pdf urls from requesting the urls from the list pages and get pdf if year in range and do not have already
'''
#done

'''
Step 4
Write failed to failed file
'''
#done  

