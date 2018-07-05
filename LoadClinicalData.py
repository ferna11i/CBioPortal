import requests as rq
import pandas as pd

url = "http://www.cbioportal.org/webservice.do?"
command = "cmd=getClinicalData&case_set_id=prad_tcga_pub_all" #prad_mskcc_2014_all

response = rq.get(url + command)
# pd.read_csv(response.content, sep='\\\\t', engine='python')

rows = str(response.content.decode("utf-8")).split("\n") #gets all the rows
header = str(rows[0]).split("\t")    #get the first row. Header
indices = []

for i, col in enumerate(header):    #i stores the index from enumerate(header)
    if 'GLEASON' in col:
        indices.append(i)

    if 'CASE_ID' in col:
        indices.append(i)

for row in rows:
    columns = str(row).split('\t')
    for index in indices:
        print("{} ".format(columns[index]), end='', flush=True)
        #print("{} ".format(index), end='')
    print()


print('Done')
# for row in rows:
#     columns = str(row).split("\t")
#     print(columns)

# Sample code
# lines = str(result.decode("utf-8")).split('\n')
# for line in lines:
#     columns = str(line).split('\t')
#     print(columns)