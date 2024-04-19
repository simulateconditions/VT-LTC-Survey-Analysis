import os
import json
import pandas as pd
import shared_functions
from PIN_code import *


L =  ['RESIDENT CARE',"RESIDENTS RIGHTS","RESIDENTS' RIGHTS",'NUTRITION','LAUNDRY','PHYSICAL','PETS','RESIDENT FUNDS']
L = L + [i.lower() for i in L]
VIOLATIONS = ['V '+L[0],'V. '+L[0],"VI. "+L[1],"VI " +L[1],"VI. " + L[2],"VI. "+L[2],'VII. '+L[3],'VII '+L[3],'VIII. '+L[4],'VIII '+L[4],'IX. '+L[5],'IX '+L[5],'X '+L[6],'X. '+L[6],'XI. '+L[7],'XI '+L[7] ]

VIOLATIONS = VIOLATIONS + ['V '+L[0+7],'V. '+L[0+7],"VI. "+L[1+7],"VI " +L[1+7],"VI. " + L[2+7],"VI. "+L[2+7],'VII. '+L[3+7],'VII '+L[3+7],'VIII. '+L[4+7],'VIII '+L[4+7],'IX. '+L[5+7],'IX '+L[5+7],'X '+L[6+7],'X. '+L[6+7],'XI. '+L[7+7],'XI '+L[7+7] ]

from datetime import date
dates = {'JANUARY':1,'FEBRUARY':2,'MARCH':3,'APRIL':4,'MAY':5,'JUNE':6,'JULY':7,'AUGUST':8,'SEPTEMBER':9,'OCTOBER':10,'NOVEMBER':11,'DECEMBER':12}

    
def get_all_letter_tags(c,letter):
    tags = set()
    for i in range(len(c)):
      
      if i<len(c) and i+1 < len(c) and i+4<=len(c):
          if c[i]==letter and c[i+1:i+4].isdigit():# and not c[i+4].isdigit():
              tags.add(c[i:i+4])
          elif i+5 <= len(c) and c[i]==letter and c[i+1]==' ' and c[i+2:i+5].isdigit():
              tags.add(c[i:i+5])
              #and not c[i+5].isdigit():
      
    if len(tags)==0: return '?'
    return ','.join(list(tags))


def get_violations(c):
    result = set()
    #result = []
    for v in VIOLATIONS:
        if v in c: 
          result.add(v)
    
    return result#','.join(list(result))


def length_of_report(c):
  L = c.split()
  possible = []
  for i in range(len(L)):
      if L[i].lower() == 'of':
          if L[i-1].isdigit() and L[i+1].isdigit():
              possible.append(L[i+1])
  counts = dict()
  for elem in possible:
      if elem in counts: counts[elem] += 1
      else: counts[elem]=1
  most = 0
  best = 0
  for elem in counts:
      if counts[elem]>most: 
        best = elem
        most = counts[elem]
  if best == 0: return '?'
  return str(int(best) + 1)


def get_date(d):
    L = d.strip().split(' ')
    month = dates[L[0]]
    
    day = int(L[1][:-1])
    year = int(L[2])
    return year,month,day

def time_elapsed(d1,d2):
    if d1=='?' or d2 == '?': return '?'
    year1,month1,day1 = get_date(d1)
    year2,month2,day2 = get_date(d2)
    t1 = date(year1,month1,day1)
    t2 = date(year2,month2,day2)
    return (t2-t1).days

def seen(s,l):
    for elem in l:
        if s in elem: return True
    return False

def populate_violations(result,violations,c):
    keys1 = ['V. RESIDENT CARE','5.3','5.8','5.9','5.10','5.15','5.18']
    if seen('RESIDENT CARE',violations): 
        result[keys1[0]] = 1
    else: result[keys1[0]] = 0
    for key in keys1[1:]:
        if key in c: result[key] = 1
        else: result[key] = 0
    keys = ['VI. RESIDENTS’ RIGHTS','VII. NUTRITION','VIII. LAUNDRY','IX. PHYSICAL', '9.11','X. PETS','XI. RESIDENT FUNDS']
    if seen(keys[0].split(' ')[-1], violations): 
        result[keys[0]] = 1
    else: result[keys[0]] = 0
    if seen(keys[1].split(' ')[-1], violations): 
        result[keys[1]] = 1
    else: result[keys[1]] = 0
    if seen(keys[2].split(' ')[-1],violations): 
        result[keys[2]] = 1
    else: result[keys[2]] = 0
    if seen(keys[3].split(' ')[-1],violations): 
        result[keys[3]] = 1
    else: result[keys[3]] = 0
    if keys[4] in c: 
        result[keys[4]] = 1
    else: result[keys[4]] = 0
    if seen(keys[5].split(' ')[-1],violations): 
        result[keys[5]] = 1
    else: result[keys[5]] = 0
    if seen(keys[6].split(' ')[-1],violations): 
        result[keys[6]] = 1
    else: result[keys[6]] = 0
    return result
#labels = ['Length of Report',]

def get_viol_bool(s):
    l = s.split(',')
    non_100_tag = 0
    for elem in l:
        c = elem[1:]
        c = c.strip()
        if c.isdigit() and int(c)>100: non_100_tag = 1
    return non_100_tag
#not using>
def rtag_in(l):
    r_tag_list = get_all_letter_tags(l,'R').split(',')
    if len(r_tag_list) ==1 and '?' in r_tag_list: return False
    else: return True

def find_next_rtag_index(c):
    letter = 'r'
    for i in range(len(c)):
        if i<len(c) and i+1 < len(c) and i+4<=len(c):
          if c[i]==letter and c[i+1:i+4].isdigit():# and not c[i+4].isdigit():
              return i
          elif i+5 <= len(c) and c[i]==letter and c[i+1]==' ' and c[i+2:i+5].isdigit():
              return i
          elif i+1<len(c) and c[i] == '\n\n' and c[i+1]=='\n': return i
          elif i+1<len(c) and c[i] == 'v' and c[i+1]=='.': return i
    return '?'
def get_og_type_survey(c,result):
    #result is the dict for this survey
    # first instance of initial comments

    c = c.lower()

    i1 = c.find('initial comments')
    
    if i1 != -1: 
        found = True
        i1 += 23
        c = c[i1:]
    else: 
        found = False
        return result
    i2 = find_next_rtag_index(c) 
    if i2 == '?':
        return result
    # else: return result
    #print(L[i])
    line = c[:i2]
    if len(line.splitlines()) > 10: line = (',').join(line.splitlines()[:10])
    
    print(line)
    print('next')
    words3 =['self-report', 'self report','self-reported' ,'self reported' , 'facility report','facility reported']
    if 'annual survey' in line or 're-licensure' in line or 'health' in line or 'relicensure' in line:
        result['Re-license Plans'] = 1
    if 'complaint' in line: result['Complaint Plans']=1
    for word in words3: 
        if word in line: result['Self Report Plans'] = 1
    if 'revisit' in line or 'follow-up' in line: result['Revisit Plans']=1


    return result


def pull_data(c,full_path='None'):
    result = dict()
    result['Facility Name'] = find_PIN(c)
    result['Type of Facility'] = None
    result['Length of Report'] = str(length_of_report(c))
    
    result['Date of Original Survey'] = shared_functions.date_of_survey(c).upper()
    result['Date of Results']=shared_functions.date_of_results(c).upper()
    result['Time Between (days)'] = None
    violations = get_violations(c)
    
    populate_violations(result,violations,c)
    result['Violations List'] = ','.join(list(violations))
    if result['Violations List'] == '': result['Violations List'] = '?'
    result['R tags']=get_all_letter_tags(c,'R')
    result['A tags']=get_all_letter_tags(c,'A')
    result['Severity Levels'] = shared_functions.get_severity(c)
    violations_bool = get_viol_bool(result['R tags'])
    if violations_bool: n = 'Y' 
    else: n = 'N'
    result['Violation Y/N'] = n 
    #print(result['R tags'],violations_bool)
    result['Type of Survey']= shared_functions.type_of_survey(c,violations_bool)
    type_survey_update = {'Re-license Plans':'?','Complaint Plans':'?','Self Report Plans':'?','Revisit Plans':'?'}
    if result['Type of Survey'] == 'Acceptable Plans':
        type_survey_update = get_og_type_survey(c,type_survey_update)
        #print(type_survey_update)
    result.update(type_survey_update)
    
    return result
  


#there is no reason not to share this function with SNF


        
       
    

      

    
#pulls SNF Survey Data from Text For Processing/SNF Survey









