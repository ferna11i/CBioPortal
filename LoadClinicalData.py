import pandas as pd
import requests as rq

def getColumnHeaders(header):         #To get the data frame of column headers. [Index, Column Name]
    columns = []
    indices = []

    for i,col in enumerate(header):
        if 'GLEASON' in col or 'CASE_ID' in col:
            columns.append(col)
            indices.append(i)

    df = pd.DataFrame(data=columns, index=indices, columns=['Names'])

    return df

def getCommonColumns(fn_table, new_df):

    column_list = []

    for table_col in fn_table.columns.values:
        for df_col in new_df.columns.values:
            if df_col in table_col:
                column_list.append(df_col)

    return column_list

url = "http://www.cbioportal.org/webservice.do?"
command = "cmd=getClinicalData&case_set_id={}_all" #Provides placeholder for study name


data_dict = {}                   #dictionary of studies , #prad_mskcc_2014_all , prad_tcga_pub_all
data_dict["prad_broad_2013"] = ""
data_dict["prad_eururol_2017"] = ""
final_table = pd.DataFrame()
merge_col = []

for study in data_dict:
    response = rq.get(url + command.format(study))    #put the study name in command & hit the web service

    rows = str(response.content.decode("utf-8")).split("\n") #gets all the rows
    header = str(rows[0]).split("\t")                        #get the first row. Header
    del rows[0]                                              #delete header row
    del rows[-1]                                             #delete last row

    header_df = getColumnHeaders(header)                     #Get column headers for each study

    # create df for data and put it in dictonary of studies
    data_dict[study] = pd.DataFrame(columns=list(header_df['Names']))

    for sentence in rows:
        row = str(sentence).split("\t")                      #get each cell
        data = []                                            #list for each row of data
        counter = len(data_dict[study])
        for index in header_df.index:
            data.append(row[index])                          #put each row in the list

        data_dict[study].loc[counter] = data

    if len(final_table) != 0:
        merge_col = getCommonColumns(final_table, data_dict[study])
        final_table = pd.merge(final_table, data_dict[study], how='outer', on=merge_col) #on=", ".join(merge_col)
    else:
        final_table = data_dict[study]


json_data = final_table.to_json(orient='index')
print(json_data)