import os
import random
from .PIN_code import *
import VTSurveyProject.rch_alr_code as rch_alr_code
import VTSurveyProject.snf_code as snf_code
import traceback
def get_all_F_tags(c):
    A = get_all_F_tags_old(c)
    B = get_all_letter_tags(c,'F')
    return A+'/'+B

def get_all_F_tags_old(c):
    F_tags = set()
    for line in c.splitlines():
        try:
            if line.startswith('F ') and line[2:2+3].isdigit() and line[5].isspace():
                F_tags.add(line[0:5])
        except: pass
        try:
            if line.startswith('{F ') and line[3:3+3].isdigit() and line[6] == '}': 
                F_tags.add(line[1:6])
        except: pass
    if len(F_tags)==0: return '?'
    return ','.join(list(F_tags))

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

def length_of_report_secondary(c):
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


def length_of_report_simple(c):
  s = 'Page 1 of '
  n = '?'
  for line in c.splitlines():
      if s in line:
          i = line.find(s)
          n = line[i+len(s):]
          break
  return n

def length_of_report(c):
    A = length_of_report_simple(c)
    B = length_of_report_secondary(c)
    return A+'/'+B

def merge_dicts(d1,d2,priority=0):
    for key in d1:
        if key == 'Facility Name':
            if d1[key] != '?' and priority == 1:
                if d2[key] != '?':
                    d1[key]=d2[key]
        if d1[key] == '?': d1[key]=d2[key]
    return d1

def shared_key_words(c,L):
    found = dict()
  
    for w in L: found[w] = 0
      
    for key in found:
        n = c.count(key)
        found[key] = n
    
    return found

def transpose(data):
    result = dict()
    #get keys
    keys = list(data[random.choice(list(data.keys()))].keys()) #why???????????????
    for key in keys:
        result[key] = dict()
    for elem in data:
        for key in data[elem]:
            result[key][elem] = data[elem][key]
    
    return result

def list_txt_files(p):
    l = []
    for filename in os.listdir(p):
        if filename.endswith('txt'): l.append(filename)
    return l

def readFile(path):
    with open(path, "r",errors='ignore') as f:
        return f.read()

MONTHS = ['january','february','march','april','may','june','july','august','september','october','november','december']
MONTHS_DICT = {'january':'1','february':'2','march':'3','april':'4','may':'5','june':'6','july':'7','august':'8','september':'9','october':'10','november':'11','december':'12'}


def get_letter_sentence(c):

  i1 = c.find('Dear')
  if i1 == -1: 
      return "?"
  i2 = i1+1
  to_find=[':','.']
  tf = 0
  while tf < 2:
    if c[i2] == to_find[tf]: tf += 1
    i2 +=1

  sentence = c[i1:i2].lower()

  return sentence

def clean_sentence(sentence):
  if sentence.endswith('.'): sentence = sentence[:-1]
  new_sentence=''
  for i in range(len(sentence)):
      if sentence[i]==' ': new_sentence = new_sentence + sentence[i]
      elif not sentence[i].isspace():
          new_sentence = new_sentence + sentence[i]
      if sentence[i]==',': new_sentence = new_sentence + ' '
      elif sentence[i] == '\n': new_sentence = new_sentence + ' '
      elif sentence[i].isspace():
          new_sentence = new_sentence + ' ' + sentence[i]
  return new_sentence


def date_of_survey(c,sentence=None):
  if sentence == None:
      sentence = get_letter_sentence(c)

  sentence = clean_sentence(sentence)
  L = sentence.split(' ')
  while '' in L:
      L.remove('')
  #(L)
  date = '?'
  for i in range(len(L)):
    word = L[i]
    if (word in MONTHS) and i<len(L)-2:
        date = MONTHS_DICT[word] +'-'+ L[i+1][:-1].strip() + '-' + L[i+2].strip()
        #date = word + L[i+1] + ' '+ L[i+2] #except the last letter of third word
        #print('HERE')
        break
  return date
  
def date_of_results(c):
  L = c.splitlines()
  for line in L:
      A = line.lower().split(' ')
      if A == []: 
          break
      word = A[0] 
      if word in MONTHS:
          return MONTHS_DICT[word] +'-'+ A[1][:-1].strip() + '-' + A[2].strip()
  return '?'  


def type_of_survey(c,violations_bool,sentence=None):
  key_words = ['revisit','health','acceptable','accepted','annual','re-licensure','complaint']
  #get first sentence of letter
  if sentence == None:
    sentence = get_letter_sentence(c)#does period at end come with last word?
  

  #type='?'
  #L = sentence.split(' ')
  S = sentence
  words1 = ['annual survey','re-licensure','re -licensure', 're- licensure','health','annual  survey','re licensure']
  words2 = ['investigation','complaint']

  #def condition2():

  if not violations_bool:
      for word in words1: 
          if word in S: return 'Health'
      for word in words2: 
          if word in S: return 'Investigation'
      if 'revisit' in S: return 'Revisit'
      else: return '?' #send to helen
  else:
      if (not 'acceptable' in S) and (not 'accepted' in S):
          for word in words1: 
              if word in S: return 'Health'
          for word in words2: 
              if word in S: return 'Investigation'
          if 'revisit' in S: return 'Revisit'
          else: return '?'

      else: return 'Acceptable Plans'

  return '?'
      
  #old code

  # for i in range(len(L)):
  #     word = L[i]
  #     for kw in key_words:
  #         if word == kw:
  #           if word=='annual' and L[i+1]=='survey':
  #               type = 'health'
  #           else: type = kw
  #           break
  
  # if type == 'acceptable' or type== 'accepted': type = type + ' plans'
  # elif type == 're-licensure': type = 'health'
  # elif type=='complaint' and 'investigation' in sentence: type = 'investigation'
  # return type    


def get_severity(c):
  result = set()
  L = c.split()
  for elem in L:
      if 'SS=' in elem: result.add(elem[3:])
  if len(result)==0: return '?'
  return ', '.join(list(result))


def pull_all_data(P,facility_type,columns_add):
    if facility_type == 'SNF':
        pull_data = snf_code.pull_data
    else: pull_data = rch_alr_code.pull_data
    #print(pull_data)
    txt1 = os.path.join(P,'txt1')
    txt2 = os.path.join(P,'txt2')
    txt3 = os.path.join(P,'txt3')
    txt1_paths = list_txt_files(txt1)
    #print('PATHS',paths)
    all_data = dict()
    #print(len(paths))
    data_pulled = dict()
    for txt_name in txt1_paths:    
        #print(data_pulled)
        pdf_path = os.path.join(P,'PDF',txt_name[:-3]+'pdf')
        try:
            path_to_txt1 = os.path.join(txt1,txt_name)
            contents1 = readFile(path_to_txt1)
            data_pulled1 = pull_data(contents1,columns_add,full_path=pdf_path)
            data_pulled = data_pulled1
            # if data_pulled1['Type of Survey'] == '*': print('XXX',pdf_path,data_pulled1['R tags'],data_pulled1['Type of Survey'])
            # if data_pulled1['Type of Survey'] == '**': print('000',pdf_path,data_pulled1['R tags'],data_pulled1['Type of Survey'])
        except Exception as e: 
            print(facility_type,'EXCEPTION',e,type(e),type(e).__name__)
            
        try:
            path_to_txt2 = os.path.join(txt2,txt_name)
            contents2 = readFile(path_to_txt2)
            data_pulled2 = pull_data(contents2,columns_add)
#            if facility_type == 'SNF':
#                print('Katja')
#                print(contents2)
            data_pulled = merge_dicts(data_pulled,data_pulled2,priority=1)
        except Exception as e:
            print(facility_type,'EXCEPTION',e,type(e),type(e).__name__)

        try:
            path_to_txt3 = os.path.join(txt3,txt_name)
            contents3 = readFile(path_to_txt3)
            
            data_pulled3 = pull_data(contents3,columns_add)
            print(data_pulled3['Severity Levels'])
            data_pulled = merge_dicts(data_pulled,data_pulled3)
        except Exception as e:
            print(facility_type,'EXCEPTION',e,type(e),type(e).__name__)
            traceback.print_exc()
        try:
            #print(data_pulled)
            data_pulled['Type of Facility'] = facility_type
            #data_pulled['Time Between (days)'] = rch_alr_code.time_elapsed(data_pulled['Date of Original Survey'],data_pulled['Date of Results'])
            all_data[txt_name] = data_pulled 
        except Exception as e: 
            print('zero data pulled',txt_name)
            print(facility_type,'EXCEPTION',e, type(e),type(e).__name__)
    #print(len(all_data),'ALL DATA')
    #line below hopefully not needed
    #all_data = update_pin(all_data,data_pulled3)
    #print('HERE')
    return all_data

