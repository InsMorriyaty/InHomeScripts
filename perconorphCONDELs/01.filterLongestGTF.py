import sys
import pickle

f1 = open(sys.argv[1],'r') # ref gtf
f2 = sys.argv[2] # ref name 

gene_info = {}
mrna_info = {}
exon_info = {}

for line in f1 :
    line = line.strip()
    if line[0] != "#" :
        kda = line.split("\t")
        info = kda[-1].split("\"")
        if kda[2] == "gene" :
            gene_info[info[1]] = info[5]
        elif kda[2] == "transcript":
            tmp = {}
            tmp["chrname"] = kda[0]
            tmp["geneid"] = info[1]
            tmp["strand"] = kda[6]
            mrna_info[info[3]] = tmp
        elif kda[2] == "exon" : 
            transid = info[3]
            if transid not in exon_info :
                tmp = {}
                tmp["locat"] = []
                tmp["length"] = []
                tmp["locat"].append((int(kda[3]),int(kda[4])))
                tmp["length"].append(int(kda[4]) - int(kda[3]))
                exon_info[transid] = tmp
            else :
                exon_info[transid]["locat"].append((int(kda[3]),int(kda[4])))
                exon_info[transid]["length"].append(int(kda[4]) - int(kda[3]))
        else :
            continue

x = {}

for i in mrna_info.keys():
    geneid = mrna_info[i]["geneid"]
    exon_set = exon_info[i]["locat"]
    exon_sum = sum(exon_info[i]["length"])
    if geneid not in x :
        tmp = {}
        tmp["exonset"] = exon_set
        tmp["exonsum"] = exon_sum
        tmp["transid"] = i
        x[geneid] = tmp
    else :
        if exon_sum > x[geneid]["exonsum"] :
            x[geneid]["exonset"] = exon_set
            x[geneid]["exonsum"] = exon_sum
            x[geneid]["transid"] = i
        else :
            continue

coords = {}
chrx = {}

longest_transid = []

for k,v in x.items() :
    longest_transid.append(v["transid"])

for i in longest_transid :
    TSS = ""
    if mrna_info[i]["strand"] == "+" :
        TSS = int(x[mrna_info[i]["geneid"]]["exonset"][0][0]) - 1 
    else :
        TSS = x[mrna_info[i]["geneid"]]["exonset"][0][1]
    TSS1 = int(TSS) + 1 
    chro = "chr"+mrna_info[i]["chrname"]
    TSSo = str(TSS)
    TSS1o = str(TSS1)
    if mrna_info[i]["geneid"] in gene_info :
        diso = gene_info[mrna_info[i]["geneid"]]
    else :
        diso = "no description"
    geneo = mrna_info[i]["geneid"]
    print(f"{chro}\t{TSSo}\t{TSS1o}\t{geneo}\t{geneo}\t{i}\t{diso}")


    chrx[i] = chro
    coords[i] = x[geneo]["exonset"]

with open(f2+'gtf_genes_coords.p','wb') as genecords :
    pickle.dump(coords, genecords,protocol=2)
with open(f2+'gtf_genes_chr.p','wb') as genechr :
    pickle.dump(chrx, genechr,protocol=2)

f1.close()
