#for helper functions in PDF_to_TXT
import os
import cv2
import numpy as np
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError
import PyPDF2

#pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def list_files():
    files_in = os.listdir()
    return files_in

def pin_search(s):
    for elem in s.split():
        if elem.isdigit()and len(elem)==4:
            return elem
    return '?'





def work(files): # survey_type):
    # path_to = '/home/katja/Desktop/helen/helen_data/%s/pdfs' %survey_type
    pins = []
    # files = list_files(path_to)
    for f in files:
        if not f.endswith('.pdf'):continue
        txt_name = f[:-3]+'txt'
        new_name = txt_name
        pdf_path = f
        
        images = pdf2image.convert_from_path(pdf_path)
        if len(images)>=2:
        	pin_im = images[1]
        	pin_im = np.array(pin_im)
        	pin_im = cv2.cvtColor(pin_im, cv2.COLOR_BGR2GRAY)
        	pin_im = pin_im[100:500,300:700]
        	_,thresh = cv2.threshold(pin_im,50,255,cv2.THRESH_BINARY)
        	images_path = 'crop_images'
        	im_name = f[:-4]+'.png'
        	
        	cv2.imwrite(os.path.join(images_path,im_name),thresh)
        	ocr_string = pytesseract.image_to_string(thresh, lang='eng')#thresh
        		#pin = pin_search(ocr_string)
        		#pins.append((pin[6:],f[:-4]))
        	file1 = open(new_name,'w')
        	file1.writelines(ocr_string)
        	file1.close()
        #except:print('Failed:',txt_name)
    #print('!!!!!!!!!!!!!!!!',survey_type)
    #print(pins)
    #return pins







L = list_files()
work(L)









