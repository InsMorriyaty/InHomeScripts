import glob
from Bio import SeqIO
import os 

files = glob.glob("busco_scg_2/*.fas")

for fil in files :
    cluster = fil.split("/")[1].replace(".faa.fas","")
    x = {record.id: str(record.seq) for record in SeqIO.parse(fil, "fasta")}
    pepout = f"align/{cluster}.pep.fa"
    cdsout = f"align/{cluster}.cds.fa"
    for k,v in x.items():
        sp_name = k.split(".")[0]
        with open(pepout,'a') as out1 :
            out1.write(f">{sp_name}\n{v}\n")
        with open(cdsout,'a') as out2 :
            ij = f"./busco_results/{sp_name}/run_lepidoptera_odb10/busco_sequences/single_copy_busco_sequences/{cluster}.cds.fa.gz"
            ik = f"./busco_results/{sp_name}/run_lepidoptera_odb10/busco_sequences/single_copy_busco_sequences/{cluster}.cds.fa"
            if not os.path.exists(ij) :
                gff = f"./busco_results/{sp_name}/run_lepidoptera_odb10/busco_sequences/single_copy_busco_sequences/{cluster}.gff"
                outp = f"./busco_results/{sp_name}/run_lepidoptera_odb10/busco_sequences/single_copy_busco_sequences/{cluster}"
                cmd0 = f"~/software/iTools_Code/iTools Fatools getCdsPep -Ref {sp_name}.rename.genome.fa -Gff {gff} -OutPut {outp}"
                cmd = f"gunzip -df {ij}"
                os.system(cmd0)
                os.system(cmd)
            cc = {record.id: str(record.seq) for record in SeqIO.parse(ik , "fasta")}
            for o,p in cc.items():
                out2.write(f">{sp_name}\n{p}\n")
