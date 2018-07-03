import requests as rq
import pandas as pd

url = "http://www.cbioportal.org/webservice.do?"
command = "cmd=getClinicalData&case_set_id=prad_mskcc_2014_all"

response = rq.get(url + command)
# pd.read_csv(response.content, sep='\\\\t', engine='python')

lines = str(response.content.decode("utf-8")).split("\n")
print(lines)

# Sample code
# lines = str(result.decode("utf-8")).split('\n')
# for line in lines:
#     columns = str(line).split('\t')
#     print(columns)