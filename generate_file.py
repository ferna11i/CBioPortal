import requests as rq
import json
import csv

url_db = "http://zheng12z.myweb.cs.uwindsor.ca/prostate%20cancer/html/db_retrieve_table_names.php"   #sends info
url_db2 = "http://zheng12z.myweb.cs.uwindsor.ca/prostate%20cancer/html/db_retrieve_customized_tables.php"

#1. get cancer studies with the required column attributes: AGE, PSA
#query = 'SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name like ("%prad%") AND TABLE_SCHEMA="ferna11i_cbioportal"' #This only finds all prostate cancer studies
query = 'SELECT s.TABLE_NAME FROM INFORMATION_SCHEMA.TABLES AS s WHERE s.TABLE_TYPE="BASE TABLE" AND EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=s.TABLE_NAME AND COLUMN_NAME LIKE "%PSA%") AND EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=s.TABLE_NAME AND COLUMN_NAME LIKE "AGE")' 
#send in requests
result = rq.post(url_db, data=json.dumps(query)) #send in requests
table_names = json.loads(result.text)				#the json array in php is parsed into a python list

#2. make the 2D array
arr = []
arr.append(['CASE_ID', 'AGE', 'Prostate Specific Antigen(NG/DL)'])	#desirable column attributes

#3. query the prostate cancer studies and add to the 2D array
for n in table_names:
	#get specific column name. We do not want FPSA/PSA values because that is a percentage, not NG/DL.
	query = 'select column_name from information_schema.columns where table_name = "' + n + '" and column_name like "%PSA%" and not column_name like "%FPSA%"'	
	result = rq.post(url_db, data=json.dumps(query)) #send in requests
	column_name = json.loads(result.text)				#the json array in php is parsed into a python list
	
#################################
#################################
###########CHANGE THIS PART ONCE THE DB IS UPDATED WITH ALL PROSTATE CANCER STUDIES
#################################
#################################
	#query = 'SELECT patientid as CASE_ID, AGE,'+column_name[0]+' as Prostate_Specific_Antigen(NG/DL) FROM `' + n + '`'
	query = 'SELECT patientid as CASE_ID, AGE FROM `patientinfo_acyc_mda_2015`'
	result = rq.post(url_db2, data=json.dumps(query)) #send in requests
	rows = json.loads(result.text)				#the json array in php is parsed into a python list
	#append results to 2D array
	for r in rows:
		temp_arr = []
		for cols in r.values():
			temp_arr.append(cols)
		arr.append(temp_arr)

print(arr)
#write list of lists to .csv file
with open("generate_file_output.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(arr)
