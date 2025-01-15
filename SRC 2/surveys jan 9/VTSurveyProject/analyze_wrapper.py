from .PDF_to_TXT import PDF_to_TXT_Wrapper
from .survey_text_analysis import data_to_json_excel

def write_file(path,contents):
    f = open(path, "w")
    f.write(contents)
    f.close()
    print(path, 'write success')

def main_analyze(columns_add, ALR,RCH,SNF):
    result = PDF_to_TXT_Wrapper(ALR,RCH,SNF)
    if result != 'STOP' : data_to_json_excel(columns_add,ALR,RCH,SNF)
    write_file('analyze_complete.txt','Testing')
