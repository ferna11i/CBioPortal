import DatabaseQueries as dq
import LoadClinicalData as lcd

#1. Get the studies         : Done
#2. Send the studies for processing to clinicial data   : done
#3. Save the studies data to database : in progress

data_dict = dq.getStudies()
lcd.processStudies(data_dict)
