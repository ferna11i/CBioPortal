import requests as req
import json

def getStudies():
    data = {"query" :"Select id,name from study where name like '%prostate%';",
            "cmd" : "getStudies"}
    response = req.post(url=url, data=json.dumps(data))

    print(response.content)


url = "http://ferna11i.myweb.cs.uwindsor.ca/CBioPortal/Services/ClinicalData.php";

# response = req.get(url)
#
# data = response.json()
# print(data)
#
# for value in data:
#     print("{} {}".format(value['ID'], value['Name']))
