import UpdatePatientData.UpdatePatientsInfo as upi


data = upi.getStudies()
data_dict = upi.getClinicalData(data)
#print(data_dict)
print(upi.updatePatientInfoTable(data_dict))