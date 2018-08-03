import pandas as pd
import requests as rq
import json


def getStudies():

    data = {"query" : "Select id from study limit 2;",
            "cmd" : "getData"}       #Query + command for retrieving data
    response = rq.post(url=url, data=json.dumps(data)) #send post request to php to get data
    result = json.loads(response.content)               #Convert json data to array

    return result                    #return data dictionary for use later


def getClinicalData(json_data):

    data_dict = {}
    command = "cmd=getClinicalData&case_set_id={}_all" #Provides placeholder for study name

    for row in json_data:
        # put the study name in command & hit the web service
        response = rq.get(cbioURL + command.format(row['id']))

        rows = str(response.content.decode("utf-8")).split("\n")  # gets all the rows
        headers = rows[0].split("\t")                             # get the header row
        headers.insert(0, "studyid")                              # first column will be study id
        del rows[0]                                               # delete header row
        del rows[-1]                                              # delete last row
        data_dict[row['id']] = pd.DataFrame(columns = headers)

        for sentence in rows:
            cells = str(sentence).split("\t")                       # get each cell
            cells.insert(0, row['id'])                              # insert study to the start
            counter = len(data_dict[row['id']])                     # get the current index of the dictionary
            data_dict[row['id']].loc[counter] = cells               # add the row

        print("{} added to dictionary".format(row['id']))

    return data_dict

def updateStudyInfoTable(data_dict):

    query = 'INSERT INTO studyinfo VALUES'
    final_query = ""

    for study in data_dict:
        final_query = final_query + query
        for i, col in enumerate(data_dict[study]['CASE_ID']):
            final_query = final_query + '("' + study + '", "' + col + '")'

            if i == len(data_dict[study]['CASE_ID']) - 1:
                final_query = final_query + ';'
            else:
                final_query = final_query + ','

    print(final_query)

    data = {"query" : final_query,
            "cmd" : "insertStudyInfoData"}       #Query + command for retrieving data
    response = rq.post(url=url, data=json.dumps(data)) #send post request to php to get data

    return response.content                    #return data dictionary for use later

#def createTables(json_data):



url = "http://ferna11i.myweb.cs.uwindsor.ca/CBioPortal/Services/ClinicalData.php";
cbioURL = "http://www.cbioportal.org/webservice.do?"
