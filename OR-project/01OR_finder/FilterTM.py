import sys 
import os
import glob

f1 = sys.argv[1]
base_name = f1.split(".")[0]

outf1 = ""
outf2 = ""
outf3 = ""

if not os.path.exists(f"{base_name}.s.filter.1.id") :
    outf1 = f"{base_name}.s.filter.1.id" #### < 5 output
    outf2 = f"{base_name}.pass.1.id" #### >=5 & <= 7  
    outf3 = f"{base_name}.b.filter.1.id" #### > 7
else :
    files = glob.glob("*.id")
    jkl = []
    for i in files :
        jkl.append(int(i.split(".")[-2]))
    number = int(max(jkl)) + 1 
    outf1 = f"{base_name}.s.filter.{number}.id"
    outf2 = f"{base_name}.pass.{number}.id"
    outf3 = f"{base_name}.b.filter.{number}.id"

with open(f1,'r') as infile , open(outf1,'w') as o1 , open(outf2,'w') as o2,open(outf3,'w') as o3 :
    for line in infile :
        line = line.strip().split()
        seq_name = line[0]
        #count = line[1:]
        count = [int(x) for x in line[1:]]
        inff = "\t".join([str(x) for x in count])
        if1 = False # pan duan 5 
        if2 = False # pan duan 7
        if3 = False
        if any(x >= 5 for x in count) :
            if1 = True 
        if all(x > 7 for x in count) :
            if2 = False
        else :
            if2 = True
        if if1 and if2 :
            o2.write(f"{line[0]}\t{inff}\n")
        elif if2 == False :
            o3.write(f"{line[0]}\t{inff}\n")
        else :
            o1.write(f"{line[0]}\t{inff}\n")
