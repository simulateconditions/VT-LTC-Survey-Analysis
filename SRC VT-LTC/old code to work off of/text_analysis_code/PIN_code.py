#hopefully wont need this function
def update_pin(d,L):
    for t in L:
        facility = t[1]
        if d[facility]['Facility Name'] =='?':
            d[facility]['Facility Name'] = t[0]
    return d

def find_PIN(c):
    key = 'PROVIDER/SUPPLIER/'
    L = c.splitlines()
    found = False
    for i in range(len(L)):
        if key in L[i]:
            found = True
            break
    if not found:
        
        return pin_search(c)
    
    for j in range(15):
        if i>=len(L):break
        line = L[i].replace('_',' ')
        line = line.split(' ')
        for elem in line:
            if elem.isdigit() and len(elem)==4:
                return elem
        i = i + 1
    return '?'


def find_PIN_snf(c):
    found = set()
    for line in c.splitlines():
        if '47' in line:
            i = line.find('47')
            try:
                if line[i:i+6].isdigit() and line[i-1].isspace() and line[i+6].isspace():
                    found.add(line[i:i+6])
            except: pass
    return ','.join(list(found))
  
  
#txt2 pin code
def pin_search(s):
    pins = []
    for elem in s.split():
        if elem.isdigit()and len(elem)==4:
            if not elem in ['2021','2022','2023']:
                pins.append(elem)
    if pins == []: return '?'
    return ('?').join(pins)


