#import sys
#sys.path.append("text_analysis_code")
import json
import pandas as pd
from .shared_functions import pull_all_data, transpose
import os



print('***This program creates a NEW excel spreadsheet based on data in txt1, txt2 and txt3, in the ALR, RCH and SNF folders.')


def update_jsons(path_to_json,new_data):
	if os.path.exists(path_to_json): 
		print('old jsons deleted')
		os.remove(path_to_json)
	with open(path_to_json,'a+') as f: #'r+' vs 'w' 'a+'
		d = new_data
		#f.seek(0)
		json.dump(d,f)
		print('new json created',path_to_json)
	return d


def get_pin_count(d):
	d = d["Facility Name"]
	missing = 0
	there = 0
	for facility in d: 
		if d[facility]=='?': missing += 1
		else: there += 1
	return (there,missing)
def data_to_json_excel(columns_add,ALR,RCH,SNF): #didn't use bools yet
	#steps :D
    print(ALR,RCH,SNF)
    ALR_PATH = os.path.join('Survey Statements','ALR')
    RCH_PATH = os.path.join('Survey Statements','RCH')
    SNF_PATH = os.path.join('Survey Statements','SNF')

	#1) do text analysis on new surveys already transposed
    if SNF:
        snf_new_data = data_main(SNF_PATH,'SNF',columns_add)
        snf_json_path = os.path.join(SNF_PATH,'snf_json.json')
        snf_json_data = update_jsons(snf_json_path,snf_new_data)
    if ALR:
        alr_new_data = data_main(ALR_PATH,'ALR',columns_add) #RCH MAIN AND ALR MAIN = SAME
        alr_json_path = os.path.join(ALR_PATH,'alr_json.json')
        alr_json_data = update_jsons(alr_json_path,alr_new_data)
    if RCH:
        rch_new_data = data_main(RCH_PATH,'RCH',columns_add)
        rch_json_path = os.path.join(RCH_PATH,'rch_json.json')
        rch_json_data = update_jsons(rch_json_path,rch_new_data)
	#pin_count = get_pin_count(alr_new_data)
	#print('ALR',len(alr_new_data))



	#2) add to respective jsons
	
	
	

	#3) create new excels out of each jsons
    excel_path_root = os.path.join('Survey Statements')
    excel_path_SNF = os.path.join(excel_path_root,'SNF_LTC_Survey_Data.xlsx')
    excel_path_ALR = os.path.join(excel_path_root,'ALR_LTC_Survey_Data.xlsx')
    excel_path_RCH = os.path.join(excel_path_root,'RCH_LTC_Survey_Data.xlsx')
	#writer = 
    
    if SNF and os.path.exists(excel_path_SNF): os.remove(excel_path_SNF)
    if ALR and os.path.exists(excel_path_ALR): os.remove(excel_path_ALR)
    if RCH and os.path.exists(excel_path_RCH): os.remove(excel_path_RCH)

    #if not (ALR==True or RCH==True or SNF==True): return
    if SNF:
        with pd.ExcelWriter(excel_path_SNF,engine='openpyxl') as writer:
            pd.read_json(snf_json_path).to_excel(writer)
    if ALR:
        with pd.ExcelWriter(excel_path_ALR,engine='openpyxl') as writer:
            pd.read_json(alr_json_path).to_excel(writer)
    if RCH: 
        with pd.ExcelWriter(excel_path_RCH,engine='openpyxl') as writer:        
            pd.read_json(rch_json_path).to_excel(writer)
    print('\n***Complete! You will find your excel at: \n', excel_path_root,'\n\n')
	


def data_main(root_path,facility_type,columns_add):
    json_data = pull_all_data(root_path,facility_type,columns_add) 
    print(len(json_data))
    try:
    	json_data = transpose(json_data)
    except: pass
    return json_data
    
        





