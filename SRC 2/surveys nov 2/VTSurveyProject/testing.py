#testing functions
from shared_functions import get_letter_sentence,date_of_survey,date_of_results,type_of_survey
from rch_alr_code import get_og_type_survey,rtag_in,find_next_rtag_index
from PIN_code import find_PIN,pin_search
s1 = '''NAME OF PROVIDER OR SUPPLIER STREET ADDRESS, CITY, STATE, ZIP CODE

101 CURRIER STREET

THE VILLAGE AT WHITE RIVER JUNCTION WHITE RIVER JUNCTION, VT 05001

SUMMARY STATEMENT OF DEFICIENCIES. PROVIDER'S PLAN OF CORRECTION (x5)
(EACH DEFICIENCY MUST BE PRECEDED BY FULL (EACH CORRECTIVE ACTION SHOULD BE COMPLETE
REGULATORY OR LSC IDENTIFYING INFORMATION) CROSS-REFERENCED TO THE APPROPRIATE. DATE
DEFICIENCY)

 

R100} Initial Comments: R100

An unannounced on-site investigation of two
facility reported incidents was conducted by the
Division of Licensing and Protection on
4/13/2023. There were regulatory deficiencies
identified as a result of the investigations which
resulted in the need for Immediate Corrective
Action to be taken by the facility. Findings include:

R132) V. RESIDENT CARE AND HOME SERVICES R132
SS=E

5.5 Special Care Units

5.6.c Ahome that has received approval to
operate a special care unit must comply with the
specifications contained in the request for see attached
approval. The home will be surveyed to
determine if the special care unit is providing the
services, staffing, training and physical
environment that was outlined in the request for
approval.

This REQUIREMENT is not met as evidenced
by:

Based on observations, interview, and record
review the facility failed to ensure that all staff
received training that is specified in their special
care unit approval request. Findings include:

Per review of the facility Special Care Unit
request for approval the staff orientation
in-service education and training is specified as
follows:

"All staff shall complete the Heartfelt Connections
Memory Care Program, a 14-hour training that
focuses on the following topics:

'''

s3 = '''DENTIFICATION NUMBER:STATEMENT OF DEFICIENCIES 
AND PLAN OF CORRECTION(X3) DATE SURVEY
       COMPLETEDPRINTED: 04/26/2023 
FORM APPROVED
(X2) MULTIPLE CONSTRUCTION
B. WING _____________________________Division of Licensing and Protection
0660 04/13/2023C
NAME OF PROVIDER OR SUPPLIER
THE VILLAGE 
AT WHITE RIVER JUNCTIONSTREET ADDRESS, CITY, STATE, ZIP CODE
101 CURRIER STREET
WHITE RIVER JUNCTION, VT  05001
PROVIDER'S PLAN OF CORRECTION
(EACH CORRECTIVE ACTION SHOULD BE 
CROSS-REFERENCED TO THE APPROPRIATE 
DEFICIENCY)(X5)
COMPLETE
DATEID
PREFIX
TAG(X4) ID
PREFIX
TAGSUMMARY STATEMENT OF DEFICIENCIES
(EACH DEFICIENCY MUST BE PRECEDED BY FULL 
REGULATORY OR LSC IDENTIFYING INFORMATION)
 R100 Initial Comments:  R100
An unannounced on-site investigation of two 
facility reported incidents was conducted by the 
Division of Licensing and Protection on 
4/13/2023. There were regulatory deficiencies 
identified as a result of the investigations which 
resulted in the need for Immediate Corrective 
Action to be taken by the facility. Findings include:
 R132
SS=EV. RESIDENT CARE AND HOME SERVICES
5.5 Special Care Units 
 5.6.c  A home that has received approval to 
operate a special care unit must comply with the 
specifications contained in the request for 
approval.  The home will be surveyed to 
determine if the special care unit is providing the 
services, staffing, training and physical 
environment that was outlined in the request for 
'''

s6 = '''An unannounced on-site investigation of two
facility reported incidents was conducted by the
Division of Licensing and Protection on
4/13/2023. There were regulatory deficiencies
identified as a result of the investigations which
resulted in the need for Immediate Corrective
Action to be taken by the facility. Findings include:

R132) V. RESIDENT CARE AND HOME SERVICES R132
SS=E

5.5 Special Care Units

5.6.c Ahome that has received approval to
operate a special care unit must comply with the'''

s8 = '''ntified:

V. RESIDENT CARE AND HOME SERVICES
'''

print('\n\n' in s8)

def test_find_next_rtag_index():
	c = s6.lower()
	i2 = find_next_rtag_index(c)
	print(i2)
	print(c[331])
#test_find_next_rtag_index()

line = '''Action to be taken by the facility. Findings include:
 R132
SS=EV. RESIDENT CARE AND HOME SERVICES'''
def test_rtag_in_line():
	L = line.splitlines()
	print(L)
	for l in L:
		print(rtag_in(l))
		print('here')

#test_rtag_in_line()

def test_get_og_survey_type():
	type_survey_update = {'Re-license Plans':'?','Complaint Plans':'?','Self Report Plans':'?','Revisit Plans':'?'}
	result = get_og_type_survey(s1,type_survey_update)
	print(result)
	result = get_og_type_survey(s3,type_survey_update)
	print(result)
	#what if facility and reported are on separate lines
#test_get_og_survey_type()

def test_PIN():
	print(pin_search(s1))

#test_PIN()
def test_sentence():
	s = get_letter_sentence(s1)
	print(repr(s))
	print('annual  survey' in s)

#test_sentence()


def test_type():
	d = type_of_survey('',0,get_letter_sentence(s1))
	print(d)

#test_type()

def test_date_results():
	d = date_of_results()
	print(d)
#test_date_results()
