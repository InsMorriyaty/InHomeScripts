import sys
import os
import glob

f1 = sys.argv[1] # genome
f2 = sys.argv[2] # prot database 
f3 = sys.argv[3] # sp name 
f4 = sys.argv[4] # PATH to script/software
f5 = sys.argv[5] # ini pep 
f6 = sys.argv[6] # ini gff
'''
cmd1 = f"singularity exec {f4}/quickprot.v1.9.0.sif quickprot.py -q {f2} -g {f1} -p {f3}  -j 2 -t 10"
os.system(cmd1)
cmd2 = f"perl {f4}/PEP_CDS_Flt.pl {f3}.longest.cds.fasta {f3}.longest.pep.fasta"
os.system(cmd2)

prdct_interval = {}
kno_interval = {}
gene_inf = {}

with open(f'{f3}.longest.cds.fasta.flt','r') as infil1 , open(f'{f3}.longest.cds.fasta','r') as infil2:
    x = []
    for line in infil1 :
        line = line.strip()
        if line[0] == ">" :
            x.append(line.replace(">",""))
    for line in infil2 :
        line = line.strip()
        if line[0] == ">" :
            line = line.split()
            if line[0].replace(">","") in x :
                name = line[-1].split("=")[1].split(":")[0]
                start = line[-1].split(":")[1].split("-")[0]
                end = line[-1].split("-")[1].split("(")[0]
                gene = line[0].replace(">","")
                gene_inf[gene] = name.split("|")[1]+"@"+start+"@"+end
                tmp = [start,end]
                if name not in prdct_interval :
                    a = []
                    a.append(tmp)
                    prdct_interval[name.split("|")[1]] = a 
                else :
                    prdct_interval[name.split("|")[1]].append(tmp)
'''
inid = []

ini_file = f"{f3}.ini.kno.id"

with open(f5,'r') as infil1 , open(f6,'r') as infil2 ,open(ini_file,'w') as outf :
    x = []
    for line in infil1 :
        line = line.strip()
        if line[0] == ">" and "LeiOR" not in line :
            x.append(line.replace(">",""))
            inid.append(line.replace(">",""))
            outf.write(line.replace(">","")+"\n")
'''
    for line in infil2 :
        line = line.strip().split("\t")
        if line[2] == "mRNA" : 
            name = line[0].split("|")[1]
            start = line[3]
            end = line[4]
            tmp = [start,end]
            if name not in kno_interval :
                a = []
                a.append(tmp)
                kno_interval[name] = a
            else :
                kno_interval[name].append(tmp)

print(prdct_interval)
print(kno_interval)

candi = []

for k,v in prdct_interval.items():
    if k not in kno_interval :
        for i in v :
            xx = k+"@"+i[0]+"@"+i[1]
            candi.append(xx)
    else :
        k_wz = kno_interval[k]
        for a in v :
            pd = []
            for b in k_wz :
                if int(a[1]) < int(b[0]) or int(a[0]) > int(b[1]) :
                    pd.append(0)
                else :
                    pd.append(1)
            if 1 not in pd :
                xx = k+"@"+a[0]+"@"+a[1]
                candi.append(xx)
print("---------")
print(candi)

id_file = f"{f3}.non-ovlap.id"
inid_file = f"{f3}.inid.id"

if not candi :
    print("未检测到新基因，退出运行")
    with open(inid_file,'w') as outf :
        for i in inid :
            outf.write(f"{i}\n")
    sys.exit()

with open(id_file,'w') as outf :
    for k,v in gene_inf.items():
        if v in candi :
            outf.write(f"{k}\n")

cmd3 = f"seqtk subseq {f3}.longest.pep.fasta.flt {f3}.non-ovlap.id > {f3}.non-ovlap.fa"
os.system(cmd3)
cmd4 = f"blastp -query {f3}.non-ovlap.fa -db /database/nr/20250215/nr  -evalue 1e-5 -out {f3}.non-ovlap.nr.blastp.output -max_target_seqs 5 -num_threads 16 -outfmt 6"
os.system(cmd4)

xfiles = glob.glob(f"/home/ug2092/software/nr_id/*")
with open("run.sh",'w') as outf :
    for i in xfiles:
        outf.write(f"python3 {f4}/PraseSeqName.py {f3}.non-ovlap.nr.blastp.output {i}\n")

cmd5 = f"parallel -j 10 < run.sh"
os.system(cmd5)
cmd6 = f"mkdir -p tmp && mv *tmp* tmp"
os.system(cmd6)
cmd61 = f"cat tmp/* > {f3}.nr.name"
os.system(cmd61)
cmd7 = f"python3 SelectOR.py {f3}.nr.name"
os.system(cmd7)
cmd8 = f"seqtk subseq {f3}.longest.pep.fasta.flt {f3}.or.id > {f3}.TM.input.pep.fa"
os.system(cmd8)
'''
