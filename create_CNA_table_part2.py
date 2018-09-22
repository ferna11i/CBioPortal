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
	
#merge_matrices merges 2 dataframe matrices together
def merge_matrices(my_matrix, temp_matrix):
	result = pd.concat([my_matrix, temp_matrix], axis=1, sort=False)
	if 'Hugo_Symbol' in result.columns:
		result.drop(column='Hugo_Symbol', inplace = True)				#removes the HUGO symbols columns
	if 'Entrez_Gene_Id' in result.columns:
		result.drop(column='Entrez_Gene_Id',inplace = True)				#removes the entrez gene id columns
	result.to_csv('prostate_compiled_cna.csv', header=False, index=True, mode='a+')	#write new file for prostate compiled studies
	del result
	gc.collect()
	
#get_studies(filename) returns an array of the study names from 'studies.txt'
def get_studies(file):
	contents = open(file).read()
	return [item for item in contents.split('\n')[:-1]]
	
studies = get_studies("studies.txt")
studies_no_entrez_gene_id = get_studies("studies_no_entrez_gene_id.txt")

df = pd.read_csv("cna_compiled_genes.csv") 
####
#3. merge tables 
####

df.columns = df.iloc[0]			#entrez gene id becomes the index values
df.drop(df.index[0], inplace = True) #drop the entrez gene from its original place
df = df.transpose()					#now, columns are the genes
df.to_csv('prostate_compiled_cna.csv', header=False, index=False, mode='w')	#write new file for prostate compiled studies

####3.a) merge tables for studies with entrez gene id
#give the dictionary index values 
df_entrez = df.copy()
entrez_gene_id = df_entrez.iloc[1]			#entrez gene row
df_entrez.columns = entrez_gene_id			#entrez gene id becomes the index values
df_entrez.drop(df_entrez.index[0], inplace = True)

counter = 0
for study in studies:					#write studies
	my_matrix = make_matrix(study, True)
	merge_matrices(df_entrez, my_matrix)
	del my_matrix	
	gc.collect()
	counter += 1
	print(str(counter) + study)
	
####3.b) merge tables for studies with only HUGO symbols
#give the dictionary index values 
df_HUGO = df.copy()
HUGO_id = df.iloc[0]			#HGNC gene row
df_HUGO.columns = HUGO_id			#HGNC gene id becomes the index values
df_HUGO.drop(df_HUGO.index[0], inplace = True)
	
for study in studies_no_entrez_gene_id:	#write studies without entrez id
	my_matrix = make_matrix(study, False)
	merge_matrices(df_HUGO, my_matrix)
	del my_matrix	
	gc.collect()
	counter += 1
	print(str(counter) + study)




