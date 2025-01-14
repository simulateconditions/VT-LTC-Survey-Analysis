#united PDF to TXT file
#copied from txt1 file that is now in archive
#to do - incorporate (1) PyPDF2_rescue and (2) get_pin_ocr_ocv
from .PDF_TXT_functions import convert, list_files,work,txt3

import os




#forget why needed...for OCV code...

def PDF_to_TXT_Wrapper(ALR,RCH,SNF):
    ALR_bool = bool(ALR)
    RCH_bool = bool(RCH)
    SNF_bool = bool(SNF)
    #root directory
    root_dir = 'Survey Statements'
    
    #PDF Files
    ALR_pdf = os.path.join('ALR','PDF')
    RCH_pdf = os.path.join('RCH','PDF')
    SNF_pdf = os.path.join('SNF','PDF')
    #PDF Files Full Path
    ALR_path = os.path.join(root_dir,ALR_pdf)
    RCH_path = os.path.join(root_dir,RCH_pdf)
    SNF_path = os.path.join(root_dir,SNF_pdf)   
    
    print('PDF files loaded:')
    if ALR_bool: 
        ALR_pdf_files = list_files(ALR_path)        
        print(len(ALR_pdf_files),' ALR files')
    if RCH_bool: 
        RCH_pdf_files = list_files(RCH_path)
        print(len(RCH_pdf_files),' RCH files')
    if SNF_bool: 
        SNF_pdf_files = list_files(SNF_path)
        print(len(SNF_pdf_files),' SNF files')



#txt1 paths
    ALR_new = os.path.join('ALR','txt1')
    RCH_new = os.path.join('RCH','txt1')
    SNF_new = os.path.join('SNF','txt1')
    ALR_path_new = os.path.join(root_dir,ALR_new)
    RCH_path_new = os.path.join(root_dir,RCH_new)
    SNF_path_new = os.path.join(root_dir,SNF_new)


#txt1 UI and Conversion!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    print('\n\n**Converting PDF to TXT with Pytesseract**\n\n')
    result = 'go'
    
    if ALR_bool:
        result = convert(ALR_pdf_files,ALR_path,ALR_path_new)
    
    if RCH_bool and result!='STOP':
        result = convert(RCH_pdf_files,RCH_path,RCH_path_new)
    
    if SNF_bool and result!='STOP':
        result = convert(SNF_pdf_files,SNF_path,SNF_path_new)

    l1 = len(os.listdir(ALR_path_new))
    l2 = len(os.listdir(RCH_path_new))
    l3 = len(os.listdir(SNF_path_new))

    print('\n Number of files in:\n\n',ALR_path_new,':',l1,'\n',RCH_path_new,':',l2,'\n',SNF_path_new,':',l3,'\n')

    if result=='STOP':
        print('program terminated')
        return 'STOP'

#txt2 UI and Conversion!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#txt2 paths
    ALR_new = os.path.join('ALR','txt2')
    RCH_new = os.path.join('RCH','txt2')
    SNF_new = os.path.join('SNF','txt2')

    ALR_path_new = os.path.join(root_dir,ALR_new)
    RCH_path_new = os.path.join(root_dir,RCH_new)
    SNF_path_new = os.path.join(root_dir,SNF_new)

    print('\n\n**Converting PDF to TXT with OpenCV**\n\n')

    ALR_bool = ALR
    if ALR_bool and result!='STOP':
        result = work(ALR_pdf_files,ALR_path,ALR_path_new)
    RCH_bool = RCH
    if RCH_bool and result!='STOP':
        result = work(RCH_pdf_files,RCH_path,RCH_path_new)
    SNF_bool = SNF
    if SNF_bool and result!='STOP':
        result = work(SNF_pdf_files,SNF_path,SNF_path_new)

    l1 = len(os.listdir(ALR_path_new))
    l2 = len(os.listdir(RCH_path_new))
    l3 = len(os.listdir(SNF_path_new))

    print('\n Number of files in:\n\n',ALR_path_new,':',l1,'\n',RCH_path_new,':',l2,'\n',SNF_path_new,':',l3,'\n')

    if result=='STOP':
        print('program terminated')
        return 'STOP'




#txt3 paths
    ALR_new = os.path.join('ALR','txt3')
    RCH_new = os.path.join('RCH','txt3')
    SNF_new = os.path.join('SNF','txt3')

    ALR_path_new = os.path.join(root_dir,ALR_new)
    RCH_path_new = os.path.join(root_dir,RCH_new)
    SNF_path_new = os.path.join(root_dir,SNF_new)


    print('\n\n**Converting PDF to TXT with PyPDF2**\n\n')

    ALR_bool = ALR
    if ALR_bool and result!='STOP':
        result = txt3(ALR_pdf_files,ALR_path,ALR_path_new)
    RCH_bool = RCH
    if RCH_bool and result!='STOP':
        result = txt3(RCH_pdf_files,RCH_path,RCH_path_new)
    SNF_bool = SNF
    if SNF_bool and result!='STOP':
        result = txt3(SNF_pdf_files,SNF_path,SNF_path_new)

    l1 = len(os.listdir(ALR_path_new))
    l2 = len(os.listdir(RCH_path_new))
    l3 = len(os.listdir(SNF_path_new))

    print('\n Number of files in:\n\n',ALR_path_new,':',l1,'\n',RCH_path_new,':',l2,'\n',SNF_path_new,':',l3,'\n')

    if result=='STOP':
        print('program terminated')
        return 'STOP'

















