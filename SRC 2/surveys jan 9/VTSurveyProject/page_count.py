import requests
def write_file(path,contents):
    f = open(path, "w")
    f.write(contents)
    f.close()
    print(path, 'write success')

def run_counts():
    L = ['alr','rch','snf']
    result = {'alr':0,'rch':0,'snf':0}
    root_url = 'https://dlp.vermont.gov/document-categories/'
    sub_link = {'alr':'alr-survey-statement','snf':'nursing-home-survey-statements','rch':'rch-survey-statements'} 
    for e in L:
        #print(e)
        link = root_url + sub_link[e] + '?page=0'
        try: 
            r = requests.get(link)
            t = r.text
            for line in t.splitlines():
                #'href="?page="'
                if  ('aria-label="Last page"' in line): result[e] = line
        except:
            print('no')
    
    for key in result:
        line = result[key]
        i=line.find('page=')
        j = i+len('page=')
        s = ''
        while True:
            elem = line[j]
            if elem.isdigit(): 
                s+= elem
                j += 1            
            else: 
                result[key]=int(s)
                break
    print(result)
    write_file('page_count_results.txt',repr(result))
    write_file('update_complete.txt','Testing')
    
#run_counts()
