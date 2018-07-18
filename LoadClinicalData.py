import requests as rq
import json

url = "http://www.cbioportal.org/webservice.do?"
command = "cmd=getClinicalData&case_set_id=prad_tcga_pub_all" #prad_mskcc_2014_all

response = rq.get(url + command)
# pd.read_csv(response.content, sep='\\\\t', engine='python')

rows = str(response.content.decode("utf-8")).split("\n") #gets all the rows
header = str(rows[0]).split("\t")    #get the first row. Header
indices = []
column_list = []
data = []

for i, col in enumerate(header):    #i stores the index from enumerate(header)
    if 'GLEASON' in col or 'CASE_ID' in col:
        indices.append(i)
        column_list.append(col)

del rows[0] #delete header row
del rows[-1] #delete last blank row

for row in rows:
    columns = str(row).split('\t')
    obj = {}
    for j, index in enumerate(indices):
        obj[column_list[j]] = columns[index]
#         print("{} ".format(columns[index]), end='', flush=True)
        #print("{} ".format(index), end='')
#     print()
    data.append(obj)

# print('Done')

json_data = json.dumps(data)
print(json_data)
print(len(data))


# for row in rows:
#     columns = str(row).split("\t")
#     print(columns)

# Sample code
# lines = str(result.decode("utf-8")).split('\n')
# for line in lines:
#     columns = str(line).split('\t')
#     print(columns)