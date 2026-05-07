import sys 

f1 = open(sys.argv[1],'r')
f2 = sys.argv[2] ### round 

count = 1

for line in f1 :
    line = line.strip()
    if line.startswith("#") :
        print(line)
    else :
        kda = line.split("\t")
        if kda[2] == "transcript" :
            g = kda[-1].split(";")[-1].replace("geneID=","")
            t = kda[-1].split(";")[0].replace("ID=","")
            print(f"{kda[0]}\t{kda[1]}\tgene\t{kda[3]}\t{kda[4]}\t{kda[5]}\t{kda[6]}\t{kda[7]}\tID=gene-{t}.splitr{f2}")
            print(f"{kda[0]}\t{kda[1]}\tmRNA\t{kda[3]}\t{kda[4]}\t{kda[5]}\t{kda[6]}\t{kda[7]}\tID={t}.splitr{f2};Parent=gene-{t}.splitr{f2}")
            e = 1 
            c = 1
            count = count + 1 
        if kda[2] == "exon" :
            t = kda[-1].replace("Parent=","")
            print(f"{kda[0]}\t{kda[1]}\texon\t{kda[3]}\t{kda[4]}\t{kda[5]}\t{kda[6]}\t{kda[7]}\tID={t}_exon_{e}.splitr{f2};Parent={t}.splitr{f2}")
            e = e + 1 
        if kda[2] == "CDS" :
            t = kda[-1].replace("Parent=","")
            print(f"{kda[0]}\t{kda[1]}\tCDS\t{kda[3]}\t{kda[4]}\t{kda[5]}\t{kda[6]}\t{kda[7]}\tID={t}_CDS_{c}.splitr{f2};Parent={t}.splitr{f2}")
            c = c + 1 

f1.close()
