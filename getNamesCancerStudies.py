import re
infile = open("cancer_studies.txt", "r")
outfile = open("cancer_studies_processed_prostate.txt", "w")
for line in infile:
        if re.match("(.*)prostate(.*)", line):
            outfile.write (line)
infile.close()
outfile.close()
