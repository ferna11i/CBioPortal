#This file takes the list of cancer studies and returns clinical data
import os
import sys
import cbioportal
import listtools

#Get the names of cancer studies into an array
infile = open("cancer_studies_processed_prostate.txt", "r")
studies=[]
for line in infile:
        studies.append(line.split('\t')[0])
infile.close()

#take the cancer study names and retrieve from CBioPortal the Clinical Data
for s in studies:
    #1) get all patient ID from 'studies_all'
    list_clinical_data = cbioportal.getClinicalData(s+'_all')
    list_clinical_data = listtools.utf8decode(list_clinical_data)
    #2) save all clinical data into a new folder 'ProstateCancer_ClinicalData'
    os.makedirs('ProstateCancer_ClinicalData', exist_ok=True)
    listtools.writeListInText(list_clinical_data, 'ProstateCancer_ClinicalData'+'\\'+s+'_ClinicalData.txt')
	#3) show all of the cases
    List_of_caselists = cbioportal.GetCaseListForCancerStudie(s)
    List_of_caselists=listtools.utf8decode(List_of_caselists)
    listtools.writeListInText(List_of_caselists, 'ProstateCancer_ClinicalData'+'\\'+s+'_CaseLists.txt')
        
