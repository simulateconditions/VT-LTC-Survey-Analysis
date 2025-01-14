# gui_scratch.py
'''Vermont Survey Statement Tool'''
from .page_count import run_counts
#from VTSurveyProject.new_pdf_download import main_download
from .new_pdf_download import main_download
from .analyze_wrapper import main_analyze
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import threading
import os
from .shared import pull_data_from_excel
from .file_IO_setup import setup_file_system
page_counts = None

alr_options = [1,2,3,4,5]
rch_options = [1,2,3,4,5]
snf_options = [1,2,3,4,5]
def write_file(path,contents):
    f = open(path, "w")
    f.write(contents)
    f.close()
    print(path, 'write success')

DOWNLOAD_THREAD = None
ANALYZE_THREAD = None

# to do - list the progress from the thread and from file io
# thread instance isAlive()

variables = dict()

def read_file(path):
    f = open(path, "r")
    return f.read()
        

class TkRootWindow():
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('VT Survey Statement Tool')
        #self.root.columnconfigure(0,weight=1)##
        self.width = 700
        self.root.geometry('%dx%d'%(self.width,self.width))
        if not ('Survey Statements' in os.listdir()):
            setup_file_system()
        self.download_button=None
        self.analyze_button=None
        self.update_button=None

    def mainloop(self):
        self.root.mainloop()
    def on_update():
        if 'update_complete.txt' in os.listdir(): os.remove('update_complete.txt')
        app_object.update_button.config(state=tk.DISABLED)
        global UPDATE_THREAD
        UPDATE_THREAD = threading.Thread(target=run_counts).start()
    def on_download():
        try: 
            t= read_file('page_count_results.txt')
            result = eval(t)
            page_counts = result
        except:
            app_object.update_button.invoke()
        if 'download_complete.txt' in os.listdir(): os.remove('download_complete.txt')
        app_object.download_button.config(state=tk.DISABLED)
        global DOWNLOAD_THREAD
        start_year = variables['Start Year'].get()
        ALR,RCH,SNF = variables['ALR Download'].get(),variables['RCH Download'].get(),variables['SNF Download'].get()
        RCH_Pages,ALR_Pages,SNF_Pages = int(variables['RCH Page Options'].get()),int(variables['ALR Page Options'].get()),int(variables['SNF Page Options'].get())
        DOWNLOAD_THREAD = threading.Thread(target=main_download,args=(variables['Query'].get(),start_year,ALR,RCH,SNF,ALR_Pages,RCH_Pages,SNF_Pages)).start()

    def on_analyze():
        if 'analyze_complete.txt' in os.listdir(): os.remove('analyze_complete.txt')
        app_object.analyze_button.config(state=tk.DISABLED)
        global ANALYZE_THREAD
        RCH,ALR,SNF = variables['RCH Analyze'].get(),variables['ALR Analyze'].get(),variables['SNF Analyze'].get()
        columns_add = variables['columns to add'].get(1.0,tk.END).split(',')
        if columns_add==[''] or columns_add==['\n']: columns_add = []
        ANALYZE_THREAD = threading.Thread(target=main_analyze,args=(columns_add,ALR,RCH,SNF)).start()


def numfilestxt(TYPE):
    p = 'Survey Statements/%s/PageLinks'%TYPE
    F = os.listdir(p)
    total = 0
    for f in F:
        i = f.find('.')
        if i != -1:
            name = f[:i]
            if f.endswith('.txt') and name.isdigit():
                content = read_file(os.path.join(p,f))
                L = eval(content)
                total += len(L)
    return total

def numfilesexcel(TYPE):
    p = 'Survey Statements/%s'%TYPE
    p2 = 'current_%s_pdf_links.xlsx'%TYPE
    if p2 in os.listdir(p):
        data = pull_data_from_excel(os.path.join(p,p2),(0,))
        return len(data)-1
    else: return 0
def test():
    print('Testing!')



def download_and_analyze():
    def update_cb_box_alr(): 
        global alr_options
        if page_counts != None:
            alr = page_counts['alr']
            if not (alr+1 in alr_options):
                alr_options+=[alr+1]
                ALR_Combo['values']=alr_options
    def update_cb_box_rch(): 
        global rch_options
        if page_counts != None:
            rch = page_counts['rch']
            if not (rch+1 in rch_options): 
                rch_options+=[rch+1]
                RCH_Combo['values']=rch_options
    def update_cb_box_snf(): 
        global snf_options
        if page_counts != None:
            snf = page_counts['snf']
            if not (snf+1 in snf_options):
                snf_options+=[snf+1]
                SNF_Combo['values']=snf_options
    def label_hover(s):
        status_label.config(text = s)
    def label_hover_leave(e):
        status_label.config(text = '')
     #stores control variables
    global variables
    global app_object
    app_object = TkRootWindow()
    
    root = app_object.root


    n = ttk.Notebook(root)
    n.pack(expand=1,fill=tk.BOTH)
    drf = ttk.Frame(n)#root)
    drf2 = ttk.Frame(n)
    n.add(drf,text='Download')
    n.add(drf2,text='Analyze')
    
    
    
    r_info = ttk.LabelFrame(drf,text='Download Options') #font=('TkDefaultFont',16))
    r_info.grid(sticky=(tk.W + tk.E),pady=20,padx=5)  

    status_label = ttk.Label(drf,text='',font=('TkDefaultFont',12),wraplength=app_object.width)
    status_label.grid(padx=10,sticky=(tk.E+tk.W))   

 
    variables['SNF Files Found'] = tk.StringVar()
    variables['SNF Files Down'] = tk.StringVar()
    variables['ALR Files Found'] = tk.StringVar()
    variables['ALR Files Down'] = tk.StringVar()
    variables['RCH Files Found'] = tk.StringVar()
    variables['RCH Files Down'] = tk.StringVar()

    variables['Query'] = tk.StringVar()
    query_label = ttk.Label(r_info,text='String Query')
    query_label.grid(row=0,column=0)
    ttk.Entry(r_info,textvariable=variables['Query']).grid(row=1,column=0,sticky=(tk.W+tk.E))

    
    message1 = 'Example Use of Query:\nchestnut-place-2024-03-06.pdf\ntype: chesnut place or 2024-03-06\ntyping chesnut place will download all surveys from chesnut place\ntyping date will download all surveys from given date\ntype chesnut for any facility with chesnut in name\ntype any substring of pdf link'
    query_label.bind("<Enter>",lambda s=message1: label_hover(message1))
    query_label.bind("<Leave>",label_hover_leave)

    #
    year_options = ['2018','2019','2020','2021','2022','2023','2024']
    variables['Start Year'] = tk.StringVar()
    ttk.Label(r_info, text='Start Year').grid(row=3,column=0)
    ttk.Combobox(r_info,textvariable=variables['Start Year'],values=year_options).grid(row=4,column=0,sticky=(tk.W+tk.E))
    variables['RCH Download'] = tk.BooleanVar(value=False)
    variables['ALR Download'] = tk.BooleanVar(value = False)
    variables['SNF Download'] = tk.BooleanVar(value = False)
    
    saved_label = ttk.Label(r_info, text='PDF Links Saved',font=('TkDefaultFont',12))
    saved_label.grid(row=6,column = 3,sticky=(tk.W + tk.E),pady=5,padx=5)
    
    message2 = 'The links are all first saved. \n\nThe loaded links correspond to the applied filters.\n\nThen, the PDF files will begin to download. Links saved page by page'
    saved_label.bind("<Enter>",lambda s=message2: label_hover(message2))
    saved_label.bind("<Leave>",label_hover_leave)

    downloaded_label = ttk.Label(r_info, text='Total PDF Downloads',font=('TkDefaultFont',12))
    downloaded_label.grid(row=6,column = 4,sticky=(tk.W + tk.E),pady=5,padx=5)
    
    message3 = 'The counts are displayed in real time.'
    downloaded_label.bind("<Enter>",lambda s=message3: label_hover(message3))
    downloaded_label.bind("<Leave>",label_hover_leave)

    shift = 1
    ttk.Checkbutton(r_info, variable=variables['RCH Download'],text = 'RCH').grid(row = 6+shift,column = 0,sticky = tk.W,pady= 5)
    ttk.Label(r_info,textvariable=variables['RCH Files Found'],borderwidth=1,relief='raised').grid(row=6+shift,column=3,padx=5)
    ttk.Label(r_info,textvariable=variables['RCH Files Down'],borderwidth=1,relief='raised').grid(row=6+shift,column=4,padx=5)

    
    
    variables['RCH Page Options'] = tk.StringVar()
    
    global RCH_Combo
    RCH_Combo = ttk.Combobox(r_info,textvariable=variables['RCH Page Options'],values=rch_options,postcommand=update_cb_box_rch)
    RCH_Combo.current(0)
    RCH_Combo.grid(row=7,column=5,sticky=(tk.E))

    ttk.Checkbutton(r_info, variable=variables['ALR Download'],text = 'ALR').grid(row = 7+shift,column = 0,sticky = tk.W,pady= 5)
    ttk.Label(r_info,textvariable=variables['ALR Files Found'],borderwidth=1,relief='raised').grid(row=7+shift,column=3,padx=5)
    ttk.Label(r_info,textvariable=variables['ALR Files Down'],borderwidth=1,relief='raised').grid(row=7+shift,column=4,padx=5)

    variables['ALR Page Options'] = tk.StringVar()
    global ALR_Combo
    ALR_Combo = ttk.Combobox(r_info,textvariable=variables['ALR Page Options'],values=alr_options,postcommand=update_cb_box_alr)
    ALR_Combo.current(0)
    ALR_Combo.grid(row=8,column=5,sticky=(tk.E))

    ttk.Checkbutton(r_info, variable=variables['SNF Download'],text = 'SNF').grid(row = 8+shift,column = 0,sticky = tk.W,pady= 5)
    ttk.Label(r_info,textvariable=variables['SNF Files Found'],borderwidth=1,relief='raised').grid(row=8+shift,column=3,padx=5)
    ttk.Label(r_info,textvariable=variables['SNF Files Down'],borderwidth=1,relief='raised').grid(row=8+shift,column=4,padx=5)

    variables['SNF Page Options'] = tk.StringVar()

    global SNF_Combo
    SNF_Combo = ttk.Combobox(r_info,textvariable=variables['SNF Page Options'],values=snf_options,postcommand=update_cb_box_snf)
    SNF_Combo.current(0)
    SNF_Combo.grid(row=9,column=5,sticky=(tk.E))

    download_button = ttk.Button(r_info,text='Download')
    download_button.grid(row = 10+shift,column=0,sticky = tk.W,padx=5,pady=5)
    download_button.configure(command=TkRootWindow.on_download)
    app_object.download_button = download_button


    update_button = ttk.Button(r_info,text='Update Page Counts')
    update_button.grid(row = 1,column=5,sticky = tk.W,padx=5,pady=5)
    update_button.configure(command=TkRootWindow.on_update)
    app_object.update_button = update_button
    
    message_update = 'Reads vermont.gov for current total page count\nselect in dropdown menus below'
    update_button.bind("<Enter>",lambda s=message_update: label_hover(message_update))
    update_button.bind("<Leave>",label_hover_leave)


    analyze = ttk.LabelFrame(drf2,text='Analyze Options') #font=('TkDefaultFont',16))
    analyze.grid(sticky=(tk.W+tk.E),pady=20,padx=5)


    variables["ALR PDF's Converted"] = tk.StringVar()
    variables["RCH PDF's Converted"] = tk.StringVar()
    variables["SNF PDF's Converted"] = tk.StringVar()
    
    variables['RCH Analyze'] = tk.BooleanVar(value=False)
    variables['ALR Analyze'] = tk.BooleanVar(value = False)
    variables['SNF Analyze'] = tk.BooleanVar(value = False)
    
    ttk.Label(analyze, text='Total PDF Conversions Completed',font=('TkDefaultFont',12)).grid(row=0,column = 1,sticky=(tk.W + tk.E),pady=5,padx=5)
    shift = 1
    ttk.Checkbutton(analyze, variable=variables['RCH Analyze'],text = 'RCH').grid(row = 0+shift,column = 0,sticky = tk.W,pady= 5)
    ttk.Label(analyze,textvariable=variables["RCH PDF's Converted"],borderwidth=1,relief='raised').grid(row=0+shift,column=1,padx=5)

    ttk.Checkbutton(analyze, variable=variables['ALR Analyze'],text = 'ALR').grid(row = 1+shift,column = 0,sticky = tk.W,pady= 5)
    ttk.Label(analyze,textvariable=variables["ALR PDF's Converted"],borderwidth=1,relief='raised').grid(row=1+shift,column=1,padx=5)

    ttk.Checkbutton(analyze, variable=variables['SNF Analyze'],text = 'SNF').grid(row = 2+shift,column = 0,sticky = tk.W,pady= 5)
    ttk.Label(analyze,textvariable=variables["SNF PDF's Converted"],borderwidth=1,relief='raised').grid(row=2+shift,column=1,padx=5)

    ttk.Label(analyze,text = 'Include Counts for: (comma separated items)').grid(row=3+shift,column = 0)
    variables['columns to add'] = tk.Text(analyze, width = 20,height=3,font=('TkDefaultFont',12))
    variables['columns to add'].grid(sticky=(tk.W + tk.E))
    
    analyze_button = ttk.Button(analyze,text = 'Analyze')
    analyze_button.grid(row = 5+shift,column = 0,sticky = tk.W,padx=5,pady=5)
    analyze_button.configure(command=TkRootWindow.on_analyze)
    app_object.analyze_button = analyze_button

    
    def check_buttons():
        files = os.listdir()
        p = 'download_complete.txt'
        if p in files:
            app_object.download_button.config(state=tk.NORMAL)
            os.remove(p)
        p = 'analyze_complete.txt'
        if p in files:
            app_object.analyze_button.config(state=tk.NORMAL)
            os.remove(p)
        p = 'update_complete.txt'
        if p in files:
            app_object.update_button.config(state=tk.NORMAL)
            os.remove(p)
            global page_counts
            t = read_file('page_count_results.txt')
            result = eval(t)
            page_counts = result            
        root.after(1000,check_buttons)
    def update_files():
        variables['SNF Files Down'].set(str(len(os.listdir('Survey Statements/SNF/PDF'))))
        variables['SNF Files Found'].set(str(numfilestxt('SNF')))    
        variables['ALR Files Down'].set(str(len(os.listdir('Survey Statements/ALR/PDF'))))
        variables['ALR Files Found'].set(str(numfilestxt('ALR')))    
        variables['RCH Files Down'].set(str(len(os.listdir('Survey Statements/RCH/PDF'))))
        variables['RCH Files Found'].set(str(numfilestxt('RCH')))  

        variables["ALR PDF's Converted"].set(str(len(os.listdir('Survey Statements/ALR/txt1'))))
        variables["RCH PDF's Converted"].set(str(len(os.listdir('Survey Statements/RCH/txt1'))))
        variables["SNF PDF's Converted"].set(str(len(os.listdir('Survey Statements/SNF/txt1'))))  
        root.update_idletasks()
        root.after(1000,update_files)
    update_files()
    check_buttons()
    def on_closing():
        global DOWNLOAD_THREAD
        global ANALYZE_THREAD 
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            write_file('kill_threads.txt','Testing')
            #delete page_count_results.txt
            root.destroy()
    root.protocol("WM_DELETE_WINDOW",on_closing)
    app_object.mainloop()
    


if os.path.exists('kill_threads.txt'):
    os.remove('kill_threads.txt')



