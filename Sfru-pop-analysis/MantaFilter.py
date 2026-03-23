import sys 
import gzip
import os

f1 = sys.argv[1]

outdir = "MantaFilterVcf"

mkdir_cmd = f"mkdir -p {outdir}"
os.system(mkdir_cmd)

fil = f"{f1}/results/variants/diploidSV.vcf.gz"
outfil = f"{outdir}/{f1}.filter.vcf"

with gzip.open(fil ,'rt') as inputf , open(outfil,'w') as outputf :
    for line in inputf :
        line = line.strip()
        if line[0] == "#" :
            outputf.write(f"{line}\n")
        else :
            kda = line.split("\t")
            if float(kda[5]) >= 20 :
                outputf.write(f"{line}\n")
            if kda[5] == "." or not kda[5].replace(".", "").isdigit():
                continue
