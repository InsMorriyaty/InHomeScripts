import sys 

f1 = sys.argv[1]

with open(f1,'r') as infile :
    for line in infile :
        line = line.strip()
        kda = line.split("\t")
        if kda[2] == "gene" :
            info = kda[-1]
            newinfo = f'gene_id "{info}";'
            kda[-1] = newinfo
            z = "\t".join(kda)
            print(z)
        elif kda[2] == "transcript":
            info = kda[-1]
            gene = info.split(".")[0]
            newinfo = f'gene_id "{gene}"; transcript_id "{info}";'
            kda[-1] = newinfo
            z = "\t".join(kda)
            print(z)
        elif kda[2] == "exon" :
            info = kda[-1].split(";")
            g = info[1].strip().lstrip()
            t = info[0].strip().lstrip()
            newinfo = f"{g}; {t};"
            kda[-1] = newinfo
            kda[-2] = "."
            z = "\t".join(kda)
            print(z)
        elif kda[2] == "CDS" :
            info = kda[-1].split(";")
            g = info[1].strip().lstrip()
            t = info[0].strip().lstrip()
            newinfo = f"{g}; {t};"
            kda[-1] = newinfo
            z = "\t".join(kda)
            print(z)
        else :
            continue
