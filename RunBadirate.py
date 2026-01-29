import sys 
import os

f1 = sys.argv[1] # gene family count 
f2 = sys.argv[2] # time tree 

title = ""
outdir = "tmp"
perl_path = "/home/ug2092/.conda/envs/badirate/bin/perl"
bdrate_path = "~/software/badirate-master/BadiRate.pl"
GR_k = 3
BR_k = 6

mkdir_commond = f"mkdir -p tmp"
os.system(mkdir_commond)

print(f"Family\tGR likelihood\tGR AIC(K = {GR_k})\tBR likelihood\tBR AIC(K = {BR_k})\tGR-BR\tBR better-fitting than GR?\tnet rate in BR(BIRTH-DEATH)\tExpand or Construct\tnet rate in BR background\tnet rate BR - net rate BR background\tMore than background")

with open(f1,'r') as sizetable :
    for line in sizetable :
        line = line.strip().split()
        if line[0] == "FamilyID" :
            title = "\t".join(line)
        else :
            sigle_out = f"tmp/{line[0]}.size"
            info = "\t".join(line)
            with open(sigle_out,'w') as sizeout :
                sizeout.write(f"{title}\n{info}\n")
            bdrate_GR_commond = f"{perl_path} {bdrate_path} -treefile {f2} -sizefile {sigle_out} > tmp/{line[0]}BDI_GR.output"
            bdrate_BR_commond = f'{perl_path} {bdrate_path} -treefile {f2} -sizefile {sigle_out} -bmodel "9->8" > tmp/{line[0]}BDI_BR.output'
            os.system(bdrate_GR_commond)
            os.system(bdrate_BR_commond)
            GR_be = False
            GR_like = ""
            with open(f"tmp/{line[0]}BDI_GR.output",'r') as GR :
                for lineGR in GR :
                    lineGR = lineGR.strip().lstrip()
                    if lineGR.startswith("OUTPUT") :
                        GR_be = True
                    if GR_be and lineGR.startswith("#Likelihood:"):
                        GR_like_tmp = lineGR.replace("#Likelihood:","")
                        GR_like = GR_like_tmp.translate(str.maketrans("", "", " \t\n\r"))
                    #if GR_be and line and not line.startswith("#") and not line.startswith("END") :
            BR_be = False
            BR_like = ""
            x = {}
            with open(f"tmp/{line[0]}BDI_BR.output",'r') as BR :
                for lineBR in BR :
                    lineBR = lineBR.strip().lstrip()
                    if lineBR.startswith("OUTPUT") :
                        BR_be = True
                    if BR_be and lineBR.startswith("#Likelihood:"):
                        BR_like_tmp = lineBR.replace("#Likelihood:","")
                        BR_like = BR_like_tmp.translate(str.maketrans("", "", " \t\n\r"))
                    if BR_be and lineBR and not lineBR.startswith("#") and not lineBR.startswith("END") :
                        info = lineBR.split()
                        if len(info) == 4:
                            net_rate = float(info[1]) - float(info[2])
                            x[lineBR[0]] = net_rate
            if len(x) == 2:
                GR_AIC = 2*GR_k - 2*float(GR_like)
                BR_AIC = 2*BR_k - 2*float(BR_like)
                AIC_del = GR_AIC - BR_AIC
                if AIC_del >= 0 :
                    info1 = "TRUE"
                if AIC_del < 0 :
                    info1 = "FALSE"
                nr_fore = x["0"]
                if nr_fore > 0 :
                    info2 = "EXPAND"
                if nr_fore < 0 :
                    info2 = "CONSTRUCT"
                if nr_fore == 0 :
                    info2 = "EQUAL"
                nr_back = x["1"] 
                nr_del = nr_fore - nr_back 
                if nr_del > 0 :
                    info3 = "TRUE"
                if nr_del < 0 :
                    info3 = "FLASE"
                if nr_del == 0:
                    info3 = "EQUAL"
                print(f"{line[0]}\t{GR_like}\t{GR_AIC}\t{BR_like}\t{BR_AIC}\t{AIC_del}\t{info1}\t{nr_fore}\t{info2}\t{nr_back}\t{nr_del}\t{info3}")
