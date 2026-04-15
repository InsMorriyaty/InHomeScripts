###### 输入文件设置：
bitacora_fasta=$1
hmm_stat=$2
sp_name=$3

#######  step 1  获取bitacora符合标准的seq id

cd ${sp_name}

mkdir -p tmp

/home/u80010049/software/phobius/phobius.pl ${bitacora_fasta} > tmp/LeiOR.OR.phobius
cat ${bitacora_fasta} | /home/u80010049/software/tmhmm-2.0c/bin/tmhmm > tmp/LeiOR.OR.tmhmm
/home/u80010049/software/TMPred-master/build/TMPred ${bitacora_fasta} -o tmp/LeiOR.OR.tmpred
python3 /home/u80010049/software/GetTMCounts.py tmp  LeiOR > tmp/LeiOR.stat

python3 ~/software/FilterTM.py tmp/LeiOR.stat > tmp/LeiOR.filter.stat

###### step 2 获取hmmsearch的 seq ID
python3 ~/software/FilterTM.py ${hmm_stat} > tmp/hmm.stat

###### step 3 获取共有ID
cat tmp/hmm.stat tmp/LeiOR.filter.stat | sort | uniq | cut -f 1 > tmp/final.ID

seqtk subseq ${bitacora_fasta} tmp/final.ID > tmp/${sp_name}.combainOR.pep.fa 

cd ..
