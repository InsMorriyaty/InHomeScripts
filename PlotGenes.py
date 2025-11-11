#######
#为gggenes绘图生成输入文件
#######
import sys 
import re
import os

f1 = sys.argv[1] # 物种名 -链接 sp1-sp2-..
f2 = sys.argv[2] # Colliner.txt
f3 = sys.argv[3] # otrhogroup

sp_lst = f1.split("-")
x = {}
og = {}

for sp in sp_lst :
    cluster_file = f"{sp}_OR_Filter_Intermediate/{sp}.OR.Filter.loact.cluster.stat.sort"
    gff_file = f"{sp}_OR_Filter_Intermediate/{sp}.final.gff"
    strand_info = {}
    tmp = {}
    with open(gff_file,'r') as ingff :
        for line in ingff :
            line = line.strip().split("\t")
            if line[2] == "mRNA" :
                gene = line[-1].split(";")[0].split("=")[1]
                strand_info[gene] = line[-3]
    with open(cluster_file,'r') as incluster :
        for line in incluster :
            line = line.strip().split("\t")
            strand = strand_info[line[0]]
            gene = ""
            if line[1] == "None" :
                gene = f"{sp}_Specfic"
            else :
                gene = line[1]
            alinfo = f"{gene}@{line[2]}@{line[3]}@{line[4]}@{strand}"
            tmp[line[0]] = alinfo 
    x[sp] = tmp

with open(f3,'r') as ogf :
    for line in ogf:
        line = line.strip().split()
        ogname = line[0].replace(":","")
        gm = line[1:]
        og[ogname] = gm

count = 1 

os.system("mkdir -p plot")

with open(f2,'r') as coli :
    for line in coli :
        line = line.strip().split()
        genome = f"GenomeCluster{count}"
        outfile = f"plot/{genome}"
        with open(outfile,'w') as outf:
            for i in line :
                if "Z" not in i :
                    species = re.sub(r'\d', '', i)
                    number = i.replace(species,"")
                    chrr = species + "Chr" + number
                else :
                    species = i.replace("Z","")
                    chrr = species + "ChrZ"
                inff = x[species]
                for a in inff :
                    kda = inff[a].split("@")
                    OG = ""
                    for m in og :
                        if a in og[m] :
                            OG = m
                            break
                    if chrr == kda[1] :
                        if kda[-1] == "+" :
                            outf.write(f"{chrr}\t{OG}\t{kda[2]}\t{kda[3]}\tforward\t1\n")
                        else :
                            outf.write(f"{chrr}\t{OG}\t{kda[2]}\t{kda[3]}\treverse\t0\n")
        count = count + 1 
            

