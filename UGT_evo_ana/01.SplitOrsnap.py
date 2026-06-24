import glob
from Bio import SeqIO

files = glob.glob("./*orthosnap*fa")

cds = {record.id: str(record.seq) for record in SeqIO.parse("ugt.cds.fa", "fasta")}
pep = {record.id: str(record.seq) for record in SeqIO.parse("ugt.pep.fa", "fasta")}

for fil in files :
    x = {record.id: str(record.seq) for record in SeqIO.parse(fil, "fasta")}
    outname = fil.split(".")[-2]
    cds_out = f"align/orthosnap.{outname}.cds.fa"
    pep_out = f"align/orthosnap.{outname}.pep.fa"
    with open(cds_out,'w') as out1 , open(pep_out,'w') as out2 :
        for i in x :
            name = i.split("|")[1]
            sp = i.split("|")[0]
            out1.write(f">{sp}\n{cds[i]}\n")
            out2.write(f">{sp}\n{pep[i]}\n")

