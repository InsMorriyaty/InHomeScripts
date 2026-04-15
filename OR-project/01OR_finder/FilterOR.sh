###########################################################
##       基于有GFF的Bitacora运行后的OR序列过滤           ##
## 首先过滤预测的OR序列，要求                            ##
##                    1） CDS为3的倍数                   ##
##                    2） 起始密码子开始                 ##
##                    3） 终止密码子结尾                 ##
## 其次基于4款软件预测跨膜结构域                         ##
##   Tmpred Hmmtop Phobius Tmhmm                         ##
## 要求，对于一个蛋白，至少一个软件预测的跨膜结构域数>=5 ##
###########################################################

###### 第一部分，指定所需软件
iTools_path=/home/u80010049/software/Reseqtools-master/iTools_Code/iTools
PEP_CDS_Flt=/home/u80010049/software/PEP_CDS_Flt.pl
#export HMMTOP_ARCH=/home/ug1708/software/insectOR/tools/hmmtop_2.1
#export LD_LIBRARY_PATH=/home/ug1708/software/insectOR/tools/TMPred/boost_1_74_0/local/lib:$LD_LIBRARY_PATH
TMPred=/home/u80010049/software/TMPred-master/build/TMPred
Phobius=/home/u80010049/software/phobius/phobius.pl
Tmhmm=/home/u80010049/software/tmhmm-2.0c/bin/tmhmm
GetTMCounts=/home/u80010049/software/GetTMCounts.py
gff_filter_longest=/home/u80010049/software/gff_filter_longest.pl
hmm=hmmsearch
hmmfile=/home/u80010049/software/bitacora-master/7tm_6/db/LeiOR_db.hmm
###### 指定输入文件
species=$1
Genome=$2
Gff=$3
mkdir -p ${species}_OR_Filter_Intermediate
###### step 1
perl $gff_filter_longest $Gff ${species}_OR_Filter_Intermediate/${species}_gene_mrna_cds.ids ${species}_OR_Filter_Intermediate/${species}.final.gff
${iTools_path} Fatools getCdsPep -Ref $Genome -Gff ${species}_OR_Filter_Intermediate/${species}.final.gff -OutPut ${species}_OR_Filter_Intermediate/${species}.OR
gunzip -f ${species}_OR_Filter_Intermediate/${species}.OR.pep.fa.gz
gunzip -f ${species}_OR_Filter_Intermediate/${species}.OR.cds.fa.gz
perl ${PEP_CDS_Flt} ${species}_OR_Filter_Intermediate/${species}.OR.cds.fa ${species}_OR_Filter_Intermediate/${species}.OR.pep.fa
###### step 2 hmm search
$hmm -o ${species}_OR_Filter_Intermediate/hmmsearch.out --tblout ${species}_OR_Filter_Intermediate/hmmsearch.tblout --cpu 5 -E 0.00001 $hmmfile ${species}_OR_Filter_Intermediate/${species}.OR.pep.fa.flt
cat ${species}_OR_Filter_Intermediate/hmmsearch.tblout | grep -v "#" | cut -f 1 | awk '{print$1}' > ${species}_OR_Filter_Intermediate/hmmsearch.ID
seqtk subseq ${species}_OR_Filter_Intermediate/${species}.OR.pep.fa.flt ${species}_OR_Filter_Intermediate/hmmsearch.ID > ${species}_OR_Filter_Intermediate/TM.input.fa

##### run 4 software
$TMPred ${species}_OR_Filter_Intermediate/TM.input.fa -o ${species}_OR_Filter_Intermediate/${species}.OR.tmpred
$Phobius ${species}_OR_Filter_Intermediate/TM.input.fa > ${species}_OR_Filter_Intermediate/${species}.OR.phobius
cat ${species}_OR_Filter_Intermediate/TM.input.fa | $Tmhmm > ${species}_OR_Filter_Intermediate/${species}.OR.tmhmm

####  Get ID 
python3 ${GetTMCounts} ${species}_OR_Filter_Intermediate ${species} > ${species}_OR_Filter_Intermediate/${species}.OR.Filter.stat

