from old_code.text_analysis_code.PIN_code import *
import os

def read_file(path):
    f = open(path, "r")
    return f.read()

p1 = 'Documents/Survey Statements/ALR/txt1'
p2 = 'Documents/Survey Statements/RCH/txt1'
p3 = 'Documents/Survey Statements/SNF/txt1'

alr_files = os.listdir(p1)
rch_files = os.listdir(p2)
snf_files = os.listdir(p3)

pin = []
print(len(snf_files))
for f in snf_files:
    content = read_file(p3+'/'+f)
    result = find_PIN_snf(content)
    if result != '?': pin.append(result)

print(pin)
