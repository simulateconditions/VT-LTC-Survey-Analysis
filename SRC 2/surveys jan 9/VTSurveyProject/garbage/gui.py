import tkinter as tk
def make_check_button(name,r,c,root):
   #checkName = tk.Label(root,text=name)
    check_value = tk.BooleanVar(value=False)
    inp2 = tk.Checkbutton(root,text=name, variable=check_value)
    #checkName.grid(row=r,column=c+1)
    inp2.grid(row=r,column=c)
    return check_value

def run():
    root = tk.Tk()
    root.title('Survey Interface')
    root.geometry('1000x800')
    root.resizable(False,False)
    
    def on_submit():
        
        entry = name_input.get()
        alr_val,rch_val,snf_val = alr.get(),rch.get(),snf.get() #not working
        #alr_pages_num,rch_pages_num,snf_pages_num = alr_pages.get(),rch_pages.get(),snf_pages.get()
        year = year_var.get()

        print(bool(alr),bool(rch),bool(snf),entry,year)
        print(var.get())
        loading_var.set('Loading')
        root.update_idletasks()
        #update canvas
        loading_var.set('Done Loading')

    loading_var = tk.StringVar(value='You have a GUI!',name='main label')
    title = tk.Label(root, textvariable=loading_var,font =('Arial 16 bold'),bg='brown',fg='#FF0')
    title.grid()
    
    entry = tk.Label(root,text='Specific Query')
    name_input = tk.Entry(root)
    entry.grid(row=0,column=1)
    name_input.grid(row=1,column=1)

    alr = make_check_button("ALR",0,2,root)
    rch = make_check_button("RCH",1,2,root)
    snf = make_check_button("SNF",2,2,root)
    
#    they all move together
#    def make_spinbox(max_allowed,r,c):
#        results = tk.Label(root,text='pages')
#        inp3 = tk.Spinbox(root,from_=1, to=max_allowed,increment=max_allowed//10,text='pages')
#        results.grid(row=r,column=c+1)
#        inp3.grid(row=r,column=c)
#        return inp3
#    
#    alr_pages = make_spinbox(13,0,3)
#    rch_pages = make_spinbox(42,1,3)
#    snf_pages = make_spinbox(132,2,3)
    
    
    yr = tk.Label(root,text='Start Year')
    year_var = tk.StringVar(value='2018')
    options = ['2018','2019','2020','2021','2022','2023','2024']
    inp4 = tk.OptionMenu(root,year_var,*options)
    

    yr.grid(row=0,column=6)
    inp4.grid(row=0,column=5)

    frame = tk.Frame(root)
    def sel():
        s = str(var.get())
    var = tk.IntVar()
    buttons = [tk.Radiobutton(frame,text='yes',variable=var,value=1,command=sel),tk.Radiobutton(frame,text='no',variable=var,value=2,command=sel)]
    frame.grid(row=1,column=0,rowspan=2)
   #i = 2
    for button in buttons: 
        button.pack()
       # i += 1

    submit_btn = tk.Button(root,text='Download')
    submit_btn.grid(row=4,column=0)
    submit_btn.configure(command=on_submit)
    
    
    root.mainloop()

run()
