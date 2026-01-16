#process file name AllClusters.txt.single.copygene.txt
import sys
import re

lis_cluster = list()
with open(sys.argv[1]) as inf:
	for lines in inf.readlines():
		line = lines.strip().split()
		line = eval(str(line).strip("[,]"))
		lis_cluster.append(line)

with open(sys.argv[2]) as inf:
	for lines in inf.readlines():
		line = lines.strip().split(":")
		cluster = line[0]
		if cluster in lis_cluster:
			genes = line[1].split()
			genes2 = ",".join(genes)
			gene_num = str(len(genes))
			species_num = str(len(genes))
			lis = [cluster,gene_num,species_num,genes2]
			print("\t".join(lis))

