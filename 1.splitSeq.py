import sys 
from Bio import SeqIO
import os 

f1 = open(sys.argv[1],'r') # scg txt 
f2 = sys.argv[2] # cds all 
f3 = sys.argv[3] # pep all 

cds = {}
pep = {}

cds = {record.id: str(record.seq) for record in SeqIO.parse(f2, "fasta")}
pep = {record.id: str(record.seq) for record in SeqIO.parse(f3, "fasta")}

for line in f1 :
    line = line.strip().split()
    og = line[0]
    commond = f"mkdir -p align/{og}"
    os.system(commond)
    cds_outputfile = f"align/{og}/cds"
    pep_outputfile = f"align/{og}/pep"
    info = line[-1].split(",")
    for i in info:
        with open(cds_outputfile,'a') as cds_out , open(pep_outputfile,'a') as pep_out :
            cds_seq = cds[i]
            pep_seq = pep[i]
            cds_out.write(f">{i}\n{cds_seq}\n")
            pep_out.write(f">{i}\n{pep_seq}\n")

f1.close()
