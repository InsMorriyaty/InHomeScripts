import glob 

files = glob.glob("align/*.stat")
x = {}

for fil in files :
    cluster = fil.split("/")[1].split(".")[-2]
    with open(fil,'r') as infil :
        for line in infil :
            lin = line.strip()
            line = line.strip().split()
            if "dN" not in line and "Node" not in lin :
                print(f"{line[0]}\tdN\t{cluster}\t{line[1]}")
                print(f"{line[0]}\tdS\t{cluster}\t{line[2]}")
                print(f"{line[0]}\tw\t{cluster}\t{line[3]}")

