#for helper functions in PDF_to_TXT
import os
import cv2
import numpy as np
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError
import PyPDF2

#pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def list_files(p):
    files_in = os.listdir(p)
    return files_in

def pin_search(s):
    for elem in s.split():
        if elem.isdigit()and len(elem)==4:
            return elem
    return '?'


#convert() sends files to txt1
def convert(files,source,destination):
    files_in_destination = list_files(destination) #clutch
    for f in files:
        if not f.lower().endswith('.pdf'):continue
        txt_name = f[:-3]+'txt'
        if txt_name in files_in_destination: continue #this line is clutch
        new_name = os.path.join(destination,txt_name)
        pdf_path = os.path.join(source,f)
        try:
            images = pdf2image.convert_from_path(pdf_path)
            result = ''''''
            for i in range(len(images)):
                pil_im = images[i] 
                ocr_string = pytesseract.image_to_string(pil_im, lang='eng')
                result = result + '\n' + ocr_string
            file1 = open(new_name,'w')
            file1.writelines(result)
            file1.close()
        except:
            print('Failed:',pdf_path)



def work(files,source,destination): # survey_type):
    # path_to = '/home/katja/Desktop/helen/helen_data/%s/pdfs' %survey_type
    pins = []
    # files = list_files(path_to)
    for f in files:
        if not f.endswith('.pdf'):continue
        files_in_destination = list_files(destination)
        txt_name = f[:-3]+'txt'
        if txt_name in files_in_destination: continue

        new_name = os.path.join(destination,txt_name)
        pdf_path = os.path.join(source,f)
        try:
        	images = pdf2image.convert_from_path(pdf_path)
        	if len(images)>=2:
        		pin_im = images[1]
        		pin_im = np.array(pin_im)
        		pin_im = cv2.cvtColor(pin_im, cv2.COLOR_BGR2GRAY)
        		pin_im = pin_im[100:500,300:700]
        		#_,thresh = cv2.threshold(pin_im,200,255,cv2.THRESH_BINARY)
        		images_path = os.path.join(destination,'crop_images')
        		im_name = f[:-4]+'.png'
        		images = list_files(images_path)
        		if im_name not in images:
        			cv2.imwrite(os.path.join(images_path,im_name),pin_im)#thresh
        		ocr_string = pytesseract.image_to_string(pin_im, lang='eng')#thresh
        		#pin = pin_search(ocr_string)
        		#pins.append((pin[6:],f[:-4]))
        		file1 = open(new_name,'w')
        		file1.writelines(ocr_string)
        		file1.close()
        except:print('Failed:',pdf_path)
    #print('!!!!!!!!!!!!!!!!',survey_type)
    #print(pins)
    #return pins




def txt3(files,source,destination):
    for f in files:
        if not f.endswith('.pdf'):continue
        files_in_destination = list_files(destination)
        txt_name = f[:-3]+'txt'
        if txt_name in files_in_destination: continue
        new_name = os.path.join(destination,txt_name)
        pdf_path = os.path.join(source,f)
        try:
            pdf_file_obj = open(pdf_path,'rb')
            pdf_reader=PyPDF2.PdfReader(pdf_file_obj)
            x = len(pdf_reader.pages)
            result = """"""
            for i in range(x):
                page_obj = pdf_reader.pages[i]
                text = page_obj.extract_text()
                result = result + '\n'+ text
            file1 = open(new_name,'w')
            file1.writelines(result)
            file1.close()
        except:print('Failed:',pdf_path)
            













