import cx_Freeze as cx

cx.setup(
    name='VTSurveyProject',
    version = '1.0',
    author = 'Simulate Conditions LLC',
    description = 'VT LTC Survey Download and Analysis GUI',
    packages = ['VTSurveyProject'],
    executables = [cx.Executable('VTSurveyProject/__main__.py',target_name='GUI')],
    options={
        'build_exe': {
            'packages': ['ssl','tkinter','threading','os','socket','datetime','random',                 'numpy','requests','certifi','idna','urllib3','pandas','pytz','tzdata','six','openpyxl','cv2','pytesseract','PIL','packaging','pdf2image','PyPDF2','typing_extensions'
                       ] ,
            'includes':['et_xmlfile','dateutil','charset_normalizer','tkinter.ttk','tkinter.messagebox','urllib.request']
                    }
            },
    silent_level='0'
    
    )

#No module named 'pandas.read_excel''pandas.read_excel', ,'pandas.DataFrame'
#
