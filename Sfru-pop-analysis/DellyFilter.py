import sys
import re

f1 = sys.argv[1]

infile = f"genotypeout/{f1}.vcf"
outfile = f"genotypeout/{f1}.filter.vcf"

with open(infile,'r') as inpuf , open(outfile,'w') as outf :
    for line in inpuf :
        line = line.strip()
        if line.startswith("#") :
            outf.write(line+"\n")
        else :
            kda = line.split("\t")
            if kda[6] == "PASS" and kda[7].split(";")[0] == "PRECISE" :
                outf.write(line+"\n")
