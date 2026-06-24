from Bio import SeqIO

pep = {record.id: str(record.seq) for record in SeqIO.parse("ugt.pep.fa", "fasta")} 

x = {}

for k,v in pep.items():
    name = k.split("|")[0]
    if name not in x :
        ifo = k+"@"+v
        tmp = []
        tmp.append(ifo)
        x[name] = tmp
    else :
        ifo = k+"@"+v
        x[name].append(ifo)

for k,v in x.items() :
    outfile = f"{k}.pep.fa"
    with open(outfile,'w') as ouf :
        for i in v :
            header = i.split("@")[0]
            seq = i.split("@")[1]
            ouf.write(f">{header}\n{seq}\n")

