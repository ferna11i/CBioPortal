import csv
import pandas as pd
import mygene 
import gc
#make_matrix(filename) returns a transposed dataframe from tables in a text file
def make_matrix(file, entrez_id_boolean):
	my_df = (pd.read_table(file)).transpose()		#dataframe needs to be transposed bc text file gives row = gene, col = patient, but we want the transposed matrix
	if entrez_id_boolean:								#studies with entrez gene id
		entrez_gene_id = my_df.iloc[1]					#entrez gene row
		my_df.columns = entrez_gene_id					#entrez gene id becomes the index values
		my_df[1] = my_df[1].str.strip()					#trim white spaces of the entrez_gene_id
		my_df.drop('Entrez_Gene_Id', inplace = True)
		my_df.drop('Hugo_Symbol', inplace = True)

	else:												#studies with only HUGO symbols
		my_df.columns = my_df.iloc[0]					#HUGO symbols become the index values
		my_df.drop('Hugo_Symbol', inplace = True)

	return my_df
	
#get_studies(filename) returns an array of the study names from 'studies.txt'
def get_studies(file):
	contents = open(file).read()
	return [item for item in contents.split('\n')[:-1]]
	
#get_gene_columns(filename) returns a dataframe of the study names from 'studies.txt'
def get_gene_columns(file, myarray, entrez_id_boolean):
	contents = open(file).read()
	temp_array = []
	exists = False

	for item in contents.split('\n'):	#gets new file's genetic ids
		item = [t.strip() for t in item.split('\t')]
		if not myarray:					#if myarray has not been initialized, directly add
			if item[0] == 'Hugo_Symbol':#first add the column attributes
				temp_array.append(['Hugo_Symbol','Entrez_Gene_Id'])
			elif entrez_id_boolean:			#studies.txt
				temp_array.append([item[0],item[1]])
			else:							#studies_no_entrez_gene_id.txt. needs to hit mygene to map hugo to entrez gene id then store
				entrez_id = (mg.query(item[0], scopes='entrezgene', species='human'))['hits']
				if not entrez_id:	#if the returned array of dictionaries is empty, then no results. append NaN
					temp_array.append([item[0], float('nan')])	#leave gene id as NaN 
				else:				#find the key:value pair 
					for d in entrez_id:		#sometimes there is more than 1 dictionary returned in the array, and only 1 dict in that contains 'entrezgene'
						if 'entrezgene' in d:#finds the dict with desired key
							temp_array.append([item[0], d['entrezgene']])	#store correct value
		else:
			if entrez_id_boolean:				#if study is from studies.txt and has entrez gene id column
				for val in myarray:				#check if this gene id exists in myarray
					try:
						if val[1] == item[1]:		#if it exists in myarray, don't add and just break
							exists = True
							break
					except IndexError:			#sometimes a study may miss the entrez gene code, such as LOCxxxxxx. use HUGO symbol instead here
						if val[0] == item[0]:
							exists = True
							break
			else:								#if study is from studies_no_entrez_gene_id.txt and doesn't have the id column, use its HUGO symbols
				for val in myarray:
					if val[0] == item[0]:
						exists = True
						break
			if not exists:						#if the gene is new, add to temp array
				if entrez_id_boolean:			#studies.txt
					temp_array.append([item[0],item[1]])
				else:							#studies_no_entrez_gene_id.txt. needs to hit mygene to map hugo to entrez gene id then store
					entrez_id = (mg.query(item[0], scopes='entrezgene', species='human'))['hits']
					if not entrez_id:	#if the returned array of dictionaries is empty, then no results. append NaN
						temp_array.append([item[0], float('nan')])	#leave gene id as NaN 
					else:				#find the key:value pair 
						for d in entrez_id:		#sometimes there is more than 1 dictionary returned in the array, and only 1 dict in that contains 'entrezgene'
							if 'entrezgene' in d:#finds the dict with desired key
								temp_array.append([item[0], d['entrezgene']])	#store correct value
		exists = False
	return myarray + temp_array
	


#merge_matrices merges 2 dataframe matrices together
def merge_matrices(my_matrix, temp_matrix):
	result = pd.concat([my_matrix, temp_matrix], axis=1, sort=False)
	result.drop(result.index[0], inplace = True)
	result.to_csv('prostate_compiled_cna.csv', header=False, index=True, mode='a+')	#write new file for prostate compiled studies
	del result
	gc.collect()
	
#### Main function:
#1. get the filenames from file
####
studies = get_studies("studies.txt")
studies_no_entrez_gene_id = get_studies("studies_no_entrez_gene_id.txt")

#### 
#2. get all the genes from all studies and merge into a dataframe
####
mg = mygene.MyGeneInfo()
myarray = []
counter = 0
for study in studies:
	myarray = get_gene_columns(study, myarray, True)
	counter += 1
	print(str(counter) + study)
for study in studies_no_entrez_gene_id:
	myarray = get_gene_columns(study, myarray, False)
	counter += 1
	print(str(counter) + study)

df = pd.DataFrame(myarray)		#convert 2D array into dictionary for easy table merging
df.drop_duplicates(inplace=True)	#delete duplicate rows of genes thanks to some studies (data_CNA_prad_mskcc_2014.txt)
df.to_csv('cna_compiled_genes.csv', header=False, index=False, mode='w')
####
#3. merge tables see part2 of create_CNA_table_part2.py
####



