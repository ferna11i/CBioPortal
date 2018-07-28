import requests as rq
import json

url = "http://www.cbioportal.org/webservice.do?"    #gets info
url_db = "http://zheng12z.myweb.cs.uwindsor.ca/prostate%20cancer/html/import_into_db.php"   #sends info

####
#table study (id, name, details)=> getCancerStudies 
####
command = "cmd=getCancerStudies"
response = rq.get(url + command)    #request from CBioPortal

#decode then parse info from cmd
string = response.content
try:
    string=string.decode('utf-8')
except UnicodeDecodeError:
    string=string.decode('latin-1')#in case there are latin-1 symbols
rows = str(string).split("\n") #gets all the rows
del rows[0]     #delete header row
del rows[-1]    #delete last blank row

for row in rows: 
    key, name, details = str(row).split("\t")
    query = 'INSERT INTO study (id, name, details) VALUES ("' + key+ '", "' + name + '", "'+details+'");'
    r = rq.post(url_db, data=json.dumps(query))

####
#table keywords (keyword, name) => getTypesOfCancer
####
command = "cmd=getTypesOfCancer"
response = rq.get(url + command)    #request from CBioPortal

#decode then parse info from cmd
string = response.content
try:
    string=string.decode('utf-8')
except UnicodeDecodeError:
    string=string.decode('latin-1')#in case there are latin-1 symbols
rows = str(string).split("\n") #gets all the rows
del rows[0]     #delete header row
del rows[-1]    #delete last blank row

for row in rows:
    keyword, name= str(row).split("\t")
    query = 'INSERT INTO keywords (keyword, name) VALUES ("' + keyword+ '", "' + name + '");'
    r = rq.post(url_db, data=json.dumps(query))
