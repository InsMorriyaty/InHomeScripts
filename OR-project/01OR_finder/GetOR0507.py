import sys 
import os 
import glob 

inistat = sys.argv[1]        # 初始TM统计 $sp.stat
inigff = sys.argv[2]        # bitacora gff
inifa = sys.argv[3]         # fasta
spname = sys.argv[4]         # 物种名

rou = 1
run = True

cmd0 = f"samtools faidx {inifa} && cut -f 1-2 {inifa}.fai > {spname}.length"

cmd1 = f"python3 ~/software/FilterTM.py {inistat}"
cmd2 = f"~/software/SelectGeneCoordsinGff.sh {spname} {inigff} {spname}.b.filter.{rou}.bed {rou}"
cmd3_0 = f"bedtools flank -i {spname}.b.filter.{rou}.bed -g {spname}.length -b 500 > {spname}.b.filter.{rou}.flank.bed"
cmd3_1 = f"cat {spname}.b.filter.{rou}.bed {spname}.b.filter.{rou}.flank.bed > {spname}.b.filter.{rou}.com.bed"
cmd3_2 = f"bedtools sort -i {spname}.b.filter.{rou}.com.bed > {spname}.b.filter.{rou}.com.sort.bed"
cmd3 = f"bedtools merge -i {spname}.b.filter.{rou}.com.sort.bed > {spname}.b.filter.{rou}.merge.bed"
cmd4 = f"bedtools getfasta -fi {inifa} -bed {spname}.b.filter.{rou}.merge.bed -fo {spname}.b.filter.{rou}.fa"
cmd5 = f"python ~/software/Tiberius/tiberius.py --genome {spname}.b.filter.{rou}.fa --model_cfg insecta --out {spname}.b.filter.{rou}.gtf"
cmd6 = f"python3 ~/software/Tiberius_GTF2GFF.py {spname}.b.filter.{rou}.gtf > {spname}.b.filter.{rou}.re.gtf"
cmd7 = f"gffread {spname}.b.filter.{rou}.re.gtf -o {spname}.b.filter.{rou}.tmp.gff3"
cmd8 = f"python3 ~/software/Tiberius_TransGFF.py {spname}.b.filter.{rou}.tmp.gff3 {rou} > {spname}.b.filter.{rou}.gff3"
cmd9 = f"python3 ~/software/TransCoordsGff.py {spname}.b.filter.{rou}.gff3 > {spname}.b.filter.{rou}.trans.gff3"
cmd10 = f"~/software/Reseqtools-master/iTools_Code/iTools Fatools getCdsPep -Ref {inifa} -Gff {spname}.b.filter.{rou}.trans.gff3 -OutPut {spname}.b.filter.{rou}"
cmd11 = f"gunzip {spname}.b.filter.{rou}.pep.fa.gz && sed -i 's/*//' {spname}.b.filter.{rou}.pep.fa && mkdir -p tmp{rou}"
cmd12 = f"/home/u80010049/software/phobius/phobius.pl {spname}.b.filter.{rou}.pep.fa > tmp{rou}/{spname}OR.phobius && cat {spname}.b.filter.{rou}.pep.fa | /home/u80010049/software/tmhmm-2.0c/bin/tmhmm > tmp{rou}/{spname}OR.tmhmm && /home/u80010049/software/TMPred-master/build/TMPred {spname}.b.filter.{rou}.pep.fa -o tmp{rou}/{spname}OR.tmpred"
cmd13 = f"python3 ~/software/GetTMCounts.py tmp{rou} {spname}OR > {spname}.{rou}.stat"
cmd14 = f"python3 ~/software/FilterTM.py {spname}.{rou}.stat"

os.system(cmd0)
os.system(cmd1)

while run :
    if os.path.getsize(f"{spname}.b.filter.{rou}.id") == 0:
        bfile = glob.glob(f"{spname}.b.filter.*.id") 
        pfile = glob.glob(f"{spname}.pass.*.id")
        sfile = glob.glob(f"{spname}.s.filter.*.id")
        al_pass = " ".join(pfile)
        cmd15 = f"cat {al_pass} > {spname}.final.id"
        os.system(cmd15)
        break
    else :
        os.system(cmd2)
        os.system(cmd3_0)
        os.system(cmd3_1)
        os.system(cmd3_2)
        os.system(cmd3)
        os.system(cmd4)
        os.system(cmd5)
        if not os.path.exists(f"{spname}.b.filter.{rou}.gtf") :
            pfile = glob.glob(f"{spname}.pass.*.id")
            al_pass = " ".join(pfile)
            cmd15 = f"cat {al_pass} > {spname}.final.id"
            os.system(cmd15)
            break
        else :
            os.system(cmd6)
            os.system(cmd7)
            os.system(cmd8)
            os.system(cmd9)
            os.system(cmd10)
            os.system(cmd11)
            os.system(cmd12)
            os.system(cmd13)
            os.system(cmd14)
            rou = rou + 1 

gfffile = glob.glob(f"*.trans.gff3")

if gfffile :
    gfffiles = " ".join(gfffile)
    cmd16 = f"cat {inigff} {gfffiles} > {spname}.com.gff3"
    cmd17 = f"python3 ~/software/Subgff.py {spname}.com.gff3 {spname}.final.id > {spname}.combain.final.gff3"
    cmd18 = f"~/software/Reseqtools-master/iTools_Code/iTools Fatools getCdsPep -Ref {inifa} -Gff {spname}.combain.final.gff3 -OutPut {spname}.final"
    cmd19 = f"gunzip {spname}.final.pep.fa.gz"
    os.system(cmd16)
    os.system(cmd17)
    os.system(cmd18)
    os.system(cmd19)
else :
    cmd17 = f"python3 ~/software/Subgff.py {inigff} {spname}.final.id > {spname}.combain.final.gff3"
    cmd18 = f"~/software/Reseqtools-master/iTools_Code/iTools Fatools getCdsPep -Ref {inifa} -Gff {spname}.combain.final.gff3 -OutPut {spname}.final"
    cmd19 = f"gunzip {spname}.final.pep.fa.gz"
    os.system(cmd17)
    os.system(cmd18)
    os.system(cmd19)
