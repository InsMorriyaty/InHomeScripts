import glob
import sys

path2file = sys.argv[1]
species = sys.argv[2]
##### deal with tmpred output 
file = f"{path2file}/{species}.OR.tmpred.tmpred"
#file = "/home/ug1708/workspace/wyj/01.smell/02annoation_pipeline/02.pipeline_test/Harmigera_OR_Filter_Intermediate/Harmigera.OR.tmpred.tmpred"
tmpred_dic = {}
pd = False
with open(file,'r') as inputf :
    for line in inputf :
        line = line.strip().lstrip()
        if line and line[0] == ">" :
            seq_name = line.replace(">","")
        if "-----> STRONGLY" in line :
            pd = True
        if pd and "strong transmembrane helices" in line :
            count = line.split()[0]
            pd = False
            tmpred_dic[seq_name] = count

### deal with phobius output 
file = f"{path2file}/{species}.OR.phobius"
#file = "Harmigera_OR_Filter_Intermediate/Harmigera.OR.phobius"
phobius = {}
with open(file,'r') as inputf :
    for line in inputf :
        line = line.strip().split()
        phobius[line[0]] = line[1]

##### deal with tmhmm output
file = f"{path2file}/{species}.OR.tmhmm"
tmmhmm = {}
with open(file,'r') as inputf :
    for line in inputf :
        line = line.strip()
        if "Number of predicted TMHs" in line :
            line = line.split()
            seq_name = line[1]
            count = line[-1]
            tmmhmm[seq_name] = count

keys_1 = list(tmpred_dic.keys())
keys_2 = list(phobius.keys())
keys_3 = list(tmmhmm.keys())
all_keys = keys_1 + keys_2 + keys_3

unique_lst = list(set(all_keys))

for i in unique_lst :
    count_lst = []
    if i in tmpred_dic:
        count_lst.append(str(tmpred_dic[i]))
    if i in phobius:
        count_lst.append(str(phobius[i]))
    if i in tmmhmm :
        count_lst.append(str(tmmhmm[i]))
    #max_count = max(count_lst)
    info = "\t".join(count_lst)
    print(f"{i}\t{info}")
