import sys 

f1 = sys.argv[1]

with open(f1,'r') as infile :
    for line in infile :
        line = line.strip().split()
        seq_name = line[0]
        count = line[1:]
        if1 = False
        if2 = False
        for i in count :
            if int(i) >= 5 :
                if1 = True
        if int(line[1]) > 7 and int(line[2]) > 7 and int(line[3]) > 7 :
            if2 = False
        else :
            if2 = True
        if if1 and if2 :
            print(f"{line[0]}\t{line[1]}\t{line[2]}\t{line[3]}")
