import sys 
import gzip 
import re

f1 = sys.argv[1]

with gzip.open(f1,'rt') as infil:
    for line in infil :
        line = line.strip()
        if line.startswith("#") :
            print(f"{line}")
        else :
            kda = line.split("\t")
            info = kda[4]
            if "AGGREGATED" not in info and "BREAKPOINT" not in info and kda[6] == "PASS" :
                tmp = kda[7]
                match = re.search(r'SVSIZE=([-+]?\d+)', tmp)
                if match :
                    svlen = int(match.group(1)) 
                    if svlen <= 2000:
                        print(line)
