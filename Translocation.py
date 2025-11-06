##########################################

#用于掉转jcvi部分染色体方向

##########################################

import sys 

length = sys.argv[1] # 染色体长度
chr_id = sys.argv[2] # 需要调整的染色体id
bed = sys.argv[3] # bed

len_dic = {}
chr_list = []

with open(length,'r') as inputfile1:
    for line in inputfile1:
        line = line.strip().split()
        len_dic[line[0]] = line[1]

with open(chr_id,'r') as inputfile2 :
    for line in inputfile2:
        line = line.strip()
        chr_list.append(line)

with open(bed,'r') as inputfile3 :
    for line in inputfile3:
        line = line.strip()
        kda = line.split()
        if kda[0] not in chr_list :
            print(line)
        else :
            new_start = int(len_dic[kda[0]]) - int(kda[2])
            new_end = int(len_dic[kda[0]]) - int(kda[1])
            new_strand = ""
            if kda[-1] == "+":
                new_strand = "-"
            else :
                new_strand = "+"
            print(f"{kda[0]}\t{new_start}\t{new_end}\t{kda[3]}\t{kda[4]}\t{new_strand}")


