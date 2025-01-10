# gui_scratch.py
'''Vermont Survey Statement Tool'''
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

    def mainloop(self):
        self.root.mainloop()

    def on_download():
        if 'download_complete.txt' in os.listdir(): os.remove('download_complete.txt')
        app_object.download_button.config(state=tk.DISABLED)
        global DOWNLOAD_THREAD
        start_year = variables['Start Year'].get()
        ALR,RCH,SNF = variables['ALR Download'].get(),variables['RCH Download'].get(),variables['SNF Download'].get()
        DOWNLOAD_THREAD = threading.Thread(target=main_download,args=(variables['Query'].get(),start_year,ALR,RCH,SNF)).start()

        #main_download(variables['Query'].get(),ALR,RCH,SNF)
    def on_analyze():
        if 'analyze_complete.txt' in os.listdir(): os.remove('analyze_complete.txt')
        app_object.analyze_button.config(state=tk.DISABLED)
        global ANALYZE_THREAD
        RCH,ALR,SNF = variables['RCH Analyze'].get(),variables['ALR Analyze'].get(),variables['SNF Analyze'].get()
        columns_add = variables['columns to add'].get(1.0,tk.END).split(',')
        if columns_add==[''] or columns_add==['\n']: columns_add = []
        ANALYZE_THREAD = threading.Thread(target=main_analyze,args=(columns_add,ALR,RCH,SNF)).start()
        #main_analyze(columns_add,ALR,RCH,SNF)
#class TkViewWindow(TkRootWindow):
#    def __init__(): return
#    def on_view():
#        print('hello')

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
    #ttk.Label(root,text="Download/Analyze Page",font=('TkDefaultFont',20)).grid()
    drf = ttk.Frame(n)#root)
    drf2 = ttk.Frame(n)
    n.add(drf,text='Download')
    n.add(drf2,text='Analyze')
    #drf.grid(padx=10,sticky=(tk.E+tk.W))
    #drf.columnconfigure(0,weight=1)
    
    
    
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

     #root.setvar(name='SNF Files,value'),master=root,name='SNF Files'
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

    ttk.Checkbutton(r_info, variable=variables['ALR Download'],text = 'ALR').grid(row = 7+shift,column = 0,sticky = tk.W,pady= 5)
    ttk.Label(r_info,textvariable=variables['ALR Files Found'],borderwidth=1,relief='raised').grid(row=7+shift,column=3,padx=5)
    ttk.Label(r_info,textvariable=variables['ALR Files Down'],borderwidth=1,relief='raised').grid(row=7+shift,column=4,padx=5)

    ttk.Checkbutton(r_info, variable=variables['SNF Download'],text = 'SNF').grid(row = 8+shift,column = 0,sticky = tk.W,pady= 5)
    ttk.Label(r_info,textvariable=variables['SNF Files Found'],borderwidth=1,relief='raised').grid(row=8+shift,column=3,padx=5)
    ttk.Label(r_info,textvariable=variables['SNF Files Down'],borderwidth=1,relief='raised').grid(row=8+shift,column=4,padx=5)

    download_button = ttk.Button(r_info,text='Download')
    download_button.grid(row = 10+shift,column=0,sticky = tk.W,padx=5,pady=5)
    download_button.configure(command=TkRootWindow.on_download)
    app_object.download_button = download_button
    #download_status_var = tk.StringVar(value='Download Status: Not started')
    #ttk.Label(r_info, textvariable=download_status_var).grid(row = 12, column = 0,sticky = (tk.E + tk.W),padx = 5,pady=10)

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
    variables['columns to add'] = tk.Text(analyze, width = 40,height=5,font=('TkDefaultFont',16))
    variables['columns to add'].grid(sticky=(tk.W + tk.E))
    
    analyze_button = ttk.Button(analyze,text = 'Analyze')
    analyze_button.grid(row = 5+shift,column = 0,sticky = tk.W,padx=5,pady=5)
    analyze_button.configure(command=TkRootWindow.on_analyze)
    app_object.analyze_button = analyze_button
    #analyze_status_var = tk.StringVar(value='Analysis Status: Not started')
    #ttk.Label(analyze, textvariable=analyze_status_var).grid(row = 7, column = 0,sticky = (tk.E + tk.W),padx = 5,pady=10)    
    
#    view = ttk.LabelFrame(drf,text='View Options') #font=('TkDefaultFont',16))
#    view.grid(sticky=(tk.W + tk.E))  
#    type_options = ['ALR','RCH','SNF']
#    variables['View Type'] = tk.StringVar()
#    ttk.Label(view, text='Facilty Type').grid(row=0,column=0)
#    ttk.Combobox(view,textvariable=variables['View Type'],values=type_options).grid(row=0,column=0,sticky=(tk.W+tk.E))
#    view_button = ttk.Button(view,text='View')
#    view_button.grid(row = 1,column=0,sticky = tk.W,padx=5,pady=5)
#    view_button.configure(command=TkViewWindow.on_view)
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
        #print('here')
        root.after(1000,update_files)
    update_files()
    check_buttons()
    def on_closing():
        global DOWNLOAD_THREAD
        global ANALYZE_THREAD 
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            write_file('kill_threads.txt','Testing')
            root.destroy()
    root.protocol("WM_DELETE_WINDOW",on_closing)
    app_object.mainloop()
    


if os.path.exists('kill_threads.txt'):
    os.remove('kill_threads.txt')
#download_and_analyze()


