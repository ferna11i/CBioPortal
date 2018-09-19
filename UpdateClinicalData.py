import json
import pymysql
import requests as rq

#To convert a string into and integer or float or stay as is
def translate(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


cbioURL = "http://www.cbioportal.org/webservice.do?"
command = "cmd=getClinicalData&case_set_id={}_all"

db = pymysql.connect('localhost','root','','cbioportal')
cursor = db.cursor(pymysql.cursors.DictCursor)
cursor.execute("Select internal_id,study_id from study")

studies = cursor.fetchall()
for study in studies:                   #Loop over each study
    response = rq.get(cbioURL + command.format(study['study_id']))

    print(study['study_id'] + " data recieved")

    try:
        rows = str(response.content.decode("utf-8")).split("\n")  # gets all the rows
    except UnicodeDecodeError:  # if the code is not in unicode
        rows = str(response.content.decode("latin-1")).split("\n")  # gets all the rows

    header = rows[0].split("\t")[1:]
    del rows[0]
    del rows[-1]

    #Note : study_id and case_id are primary keys.
    insert_str = "INSERT INTO clinical_data(study_id,case_id,attributes) VALUES"
    update_str = "ON DUPLICATE KEY UPDATE attributes = VALUES(attributes)"  #Updates the attributes if keys exist

    for i,sentence in enumerate(rows):
        case_id = str(sentence).split("\t")[0]     #Get the case id of each row
        cells = str(sentence).split("\t")[1:]       #Reading attributes of study other than case_id
        obj = {}                                    #Start creating dictionary
        for j,col in enumerate(header):
            obj[col] = translate(cells[j])

        insert_str += "(" + str(study['internal_id']) + ",'" + case_id + "','" + json.dumps(obj) + "')"
        insert_str +=  "," if (i < len(rows) - 1) else " "


    insert_str += update_str

    print(study['study_id'] + " insert begin")

    try:
        cursor.execute(insert_str)
        db.commit()
    except Exception as e:
        print(e)

    print(study['study_id'] + " insert done")