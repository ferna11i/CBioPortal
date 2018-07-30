import requests as req
import json

def getStudies():

    data_dict = {}      #dictionary for loading clinical data

    data = {"query" :"Select id,name from study where name like '%prostate%';",
            "cmd" : "getData"}       #Query + command for retrieving data
    response = req.post(url=url, data=json.dumps(data)) #send post request to php to get data
    result = json.loads(response.content)         #Convert json data to array

    for row in result:
        data_dict[row['id']] = ""       #Fill blank values now. DF's will be added later

    return data_dict                    #return data dictionary for use later


def updateGleasonScore(jsonData):

    data = {"query" :"Update data_objects set data = '{}' where tag = 'gleason';".format(jsonData),
            "cmd" : "updateData"}       #Query + command for retrieving data

    response = req.post(url=url, data=json.dumps(data))

    print(response.content)


url = "http://ferna11i.myweb.cs.uwindsor.ca/CBioPortal/Services/ClinicalData.php";

