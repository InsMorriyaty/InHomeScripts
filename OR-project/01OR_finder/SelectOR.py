import sys 

f1 = sys.argv[1] 

words = ["odorant","olfactory","OR"]

name = f1.split(".")[0]
outname1 = f"{name}.or.id"
outname2 = f"{name}.notor.id"

x = {}

with open(f1,'r') as infile1 :
    for line in infile1 :
        line = line.strip().split()
        inof = line[1:]
        seq = line[0]
        if seq not in x :
            tmp = []
            tag = ""
            for a in inof :
                if a in words :
                    tag = "y"
            tmp.append(tag)
            x[seq] = tmp 
        else :
            for a in inof :
                if a in words :
                    tag = "y"
            x[seq].append(tag)
print(x)
with open(outname1 , 'w') as out1, open(outname2,'w') as out2 :
    for k,v in x.items():
        if "y" in v :
            out1.write(f"{k}\n")
        else :
            out2.write(f"{k}\n")
