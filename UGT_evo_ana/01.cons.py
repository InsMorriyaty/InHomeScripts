import glob 
from Bio import SeqIO

files = glob.glob("align/*.fas")

x = {}

for i in files :
    cds = {record.id: str(record.seq) for record in SeqIO.parse(i, "fasta")}
    for k,v in cds.items():
        name = k
        if name not in x :
            x[name] = v 
        else :
            new_seq = x[name] + v 
            x[name] = new_seq

for k,v in x.items():
    print(f">{k}\n{v}")
