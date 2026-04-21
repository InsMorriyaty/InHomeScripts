import sys, gzip
from pathlib import Path

f1 = sys.argv[1] # ref name 
f2 = sys.argv[2] # ref gtf gz file 

outdir = "./"


outstreams = {}

features = {"CDS": f"{f1}_codingExons.bed", 
            "nonCodingExon": f"{f1}_nonCodingExons.bed", 
            "five_prime_utr": f"{f1}_5UTR.bed", 
            "three_prime_utr": f"{f1}_3UTR.bed"}

for f in features:
    outstream = open(outdir+features[f], "w")
    outstreams[f] = outstream


with open(f2, "rt") as gtf:

    for line in gtf:
        if "#"  in line:
            continue

        words = line.strip().split("\t")
        chrom = "chr"+words[0]
        start = int(words[3])-1 # convert to 0-based
        end = words[4]
        geneID = words[8].split("\"")[1] + "_" + words[8].split("\"")[3]
        featureType = words[2]

        printMe = False


        if "utr" in featureType:
            outfile = outstreams[featureType]
            printMe = True
        elif featureType == "CDS":
            outfile = outstreams[featureType]
            printMe = True
        elif (featureType == "exon") and ("mRNA" not in line):
            outfile = outstreams["nonCodingExon"]
            printMe = True

        if printMe:
            print("\t".join([chrom, str(start), end, geneID]), file=outfile)


for stream in outstreams:
    outstreams[stream].close()
