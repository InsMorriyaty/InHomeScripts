import sys 

f1 = sys.argv[1]

jg = 1
leng = 2
start = 1
end = 3
chrr = ""

with open(f1,'r') as inputf :
    for line in inputf :
        line = line.strip().split()
        if line[0] != chrr :
            tmp_start = start
            tmp_end = end 
            print(f"{line[0]}\t{line[1]}\t{start}\t{end}\t{line[-2]}\t{line[-1]}")
            tmp_start = tmp_end + jg
            tmp_end = tmp_start + leng
            chrr = line[0]
        else :
            print(f"{line[0]}\t{line[1]}\t{tmp_start}\t{tmp_end}\t{line[-2]}\t{line[-1]}")
            tmp_start = tmp_end + jg
            tmp_end = tmp_start + leng
            chrr = line[0]


