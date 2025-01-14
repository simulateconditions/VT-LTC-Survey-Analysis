import os
import json
import pandas as pd

import VTSurveyProject.shared_functions as shared_functions


from .PIN_code import *

VIOLATIONS = ['483.10','483.12','483.15','483.20','483.21','483.24','483.25','483.30','483.35','483.40','483.45','483.50','483.55','483.60','483.65','483.70','483.75','483.80','483.85','483.90','483.95']

MONTHS = ['january ','february ','march ','april ','may ','june ','july ','august ','september ','october ','november ','december ']

def list_txt_files(p):
    l = []
    for filename in os.listdir(p):
        if filename.endswith('txt'): l.append(filename)
    return l
def readFile(path):
    with open(path, "r",errors='ignore') as f:
        return f.read()

  

  
def get_violations(c):
    result = []
    #result = []
    for v in VIOLATIONS:
        if v in c:  
          result.append(v)
    if len(result)==0:return '?'
    return ','.join(result)
  



#words = ["contracted"]#,"agency associate","allegation","altercation","shortages","accident hazard", "accident hazards" ,"falls prevention","psychotropic","physical restraint","lap restraint","GDR"]
#moved words into function
  
#asdfasdfa
#asdfasdfas
"""asdfasdfasdf
asdfasdf
asdfasd"""



def get_viol_bool(s):
    l = s.split(',')
    non_000_tag = 0
    for elem in l:
        c = elem.strip()
        c = elem[1:]
        c = c.strip()
        if c.isdigit() and int(c)>0: non_000_tag = 1
    return non_000_tag

def pull_data(c,columns_add,full_path='None'):
    result = dict()
    result['Length of Report'] = shared_functions.length_of_report(c)
    result['Violations'] = get_violations(c)
    result['F tags'] = shared_functions.get_all_F_tags(c)
    result['Facility Name'] = find_PIN_snf(c)
    
    result['Date of Original Survey'] = shared_functions.date_of_survey(c)
    result['Date of Results'] = shared_functions.date_of_results(c)
    result['Severity Levels'] = shared_functions.get_severity(c)
    violations_bool = get_viol_bool(result['F tags'])
    result['Violations Y/N'] = violations_bool #'Y' if (violations_bool or len(result['Violations'].split(','))>0) else 'N'
    if result['Violations']!= '': result['Violations Y/N'] = 1
    result['Type of Survey'] = shared_functions.type_of_survey(c,violations_bool)
    
    words = ["contracted"]
    shared_key_words = shared_functions.shared_key_words
    print(columns_add,'***********************************************')
    key_word_search = shared_key_words(c,columns_add+words) #any words to always search should go in words
    for key in key_word_search:
      result[key] = key_word_search[key]
    return result
  


#pulls SNF Survey Data from Text For Processing/SNF Survey


