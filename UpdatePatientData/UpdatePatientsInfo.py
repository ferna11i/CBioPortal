import pandas as pd
import requests as rq
import json


def getStudies():

    data = {"query" : "select * from study limit 93,1;",
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

        try:
            rows = str(response.content.decode("utf-8")).split("\n")  # gets all the rows
        except UnicodeDecodeError:                                      # if the code is not in unicode
            rows = str(response.content.decode("latin-1")).split("\n")  # gets all the rows

        headers = rows[0].split("\t")                             # get the header row
        headers[0] = "patientid"                                  # rename case id to patientid column
        del rows[0]                                               # delete header row
        del rows[-1]                                              # delete last row

        for i,col in enumerate(headers):
            if len(col) > 20:                                      #keeping the length of the header at 20
                headers[i] = col[:20].replace(" ","")              #reducing the length of header.
                                                                   #removing unnecessary white spaces

        data_dict[row['id']] = pd.DataFrame(columns = headers)

        for sentence in rows:
            cells = str(sentence).split("\t")                       # get each cell
            for i,cell in enumerate(cells):                         # cleaning rows
                cells[i] = cell.replace('"','')                     # remove quotes from start and end

            counter = len(data_dict[row['id']])                     # get the current index of the dictionary
            data_dict[row['id']].loc[counter] = cells               # add the row

        print("{} added to dictionary".format(row['id']))

    return data_dict

def updatePatientInfoTable(data_dict):

    # query = 'INSERT INTO studyinfo VALUES'
    final_query = ""

    for study in data_dict:
        create_query = "Create table patientinfo_" + study + "(patientid VARCHAR(100) NOT NULL PRIMARY KEY,"

        columns = list(data_dict[study].columns.values)
        for i, col in enumerate(columns[1:]):
            create_query += col + " VARCHAR(255)"
            if i == len(columns) - 2:
                create_query += ');'
            else:
                create_query += ','

        # final_query = final_query + query
        # for i, col in enumerate(data_dict[study]['CASE_ID']):
        #     final_query = final_query + '("' + study + '", "' + col + '")'
        #
        #     if i == len(data_dict[study]['CASE_ID']) - 1:
        #         final_query = final_query + ';'
        #     else:
        #         final_query = final_query + ','

        insert_query = "INSERT INTO patientinfo_"+study+" VALUES "

        for i, row in enumerate(data_dict[study].values):
            insert_query += "("
            for j, data in enumerate(row):
                insert_query += "\"" + data
                if j == len(row) - 1:
                    insert_query += "\"),"
                else:
                    insert_query += "\","

            if i == len(data_dict[study].values) - 1:       #replace last , with ;
                insert_query = insert_query[:-1] + ";"

        final_query += create_query + insert_query

    print(final_query)

    data = {"query" : final_query,
            "cmd" : "createStudyInfoData"}       #Query + command for retrieving data
    response = rq.post(url=url, data=json.dumps(data)) #send post request to php to get data

    return response.content                    #return data dictionary for use later



# url = "http://ferna11i.myweb.cs.uwindsor.ca/CBioPortal/Services/ClinicalData.php";
url = "https://cbioportal.000webhostapp.com/ClinicalData.php"
cbioURL = "http://www.cbioportal.org/webservice.do?"
