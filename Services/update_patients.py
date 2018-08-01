import requests as rq
import json

url = "http://www.cbioportal.org/webservice.do?"    #gets info
url_db = "http://zheng12z.myweb.cs.uwindsor.ca/prostate%20cancer/html/import_into_db.php"   #sends info

####
#table studyinfo (studyid, patientid) AND patientinfo(patientid, json[column attributes])
####
command = "cmd=getCancerStudies"
response = rq.get(url + command)    #request from CBioPortal

#decode then parse info from cmd
string = response.content
try:
    string=string.decode('utf-8')
except UnicodeDecodeError:
    string=string.decode('latin-1') #in case there are latin-1 symbols
rows = str(string).split("\n")      #gets all the rows
del rows[0]                         #delete header row
del rows[-1]                        #delete last blank row

#1. get cancer studies
for row in rows:        
    key, name, details = str(row).split("\t")
    key2 = key+"_all"    #key2 = gets study id by appending string 'all', but stores without the 'all'
    print(key2)

    #2. use cancer study name to retrieve list of patients
    command2 = "cmd=getClinicalData&case_set_id="
    response2 = rq.get(url + command2 + key2)#request from CBioPortal
    
    string2 = response2.content             #decode then parse info from cmd
    try:
        string2=string2.decode('utf-8')
    except UnicodeDecodeError:
        string2=string2.decode('latin-1')   #in case there are latin-1 symbols
    rows2 = str(string2).split("\n")        #gets all the rows of patients
    header = str(rows2[0]).split("\t")      #get the column attributes

    #3. upload info about patients from current study to db tables    
    indices=[]  #stores index for columns[]. 1 to n-1 for 3b)
    columns=[]  #stores attributes. 1 to n-1 of the original columns, hence later use 0 to n-2 for 3b)
    for i, attribute in enumerate(header, start=0): #index from 0 to n-1
        if (i>0):
            indices.append(i)
            columns.append(attribute)#do not append the first column = case id
    del rows2[0]                    #delete header row
    del rows2[-1]                   #delete last blank row

    #3a) table studyinfo (studyid[id], patientid). 
    for r2 in rows2: 
        col = str(r2).split('\t')  #1 to n-1
        query = 'INSERT INTO studyinfo (studyid, patientid) VALUES ("' + key + '", "' + col[0] + '");'
        r = rq.post(url_db, data=json.dumps(query))

    #3b.1) create table for each study -> 'patientinfo_studyid'
    create_table = 'CREATE TABLE patientinfo_'+key2 +' (patientid VARCHAR(100) NOT NULL, PRIMARY KEY (patientid)'
    for attributes in columns:
        create_table += ', ' +attributes.lower() + ' TEXT' 
    create_table += ');'
    r = rq.post(url_db, data=json.dumps(create_table))#create table with the header's attribute columns

    #3b.2) populate tables for each study
    for r2 in rows2: 
        col = str(r2).split('\t')  #1 to n-1
        query = 'INSERT INTO patientinfo_'+key2+' VALUES (';
        query += '"'+col[0]+'"'
        for c in col[1:]: 
            query += ', "'+c+'"'                           #populate the table with rows of patient data
        query += ');'
        r = rq.post(url_db, data=json.dumps(query))


