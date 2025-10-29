#!/bin/bash

# Include the folder containing the FPDB databases (Including a fasta and HMM file named as YOURFPDB_db.fasta and YOURFPDB_db.hmm); Multiple FPDB can be included in the folder to be searched
#QUERYDIR=/home/ug1708/workspace/wyj/A.UGTdatabase/DB
QUERYDIR=/home/ug1708/workspace/wyj/01.smell/Dro_db
#specified perl scripts folder
PerlLib=/home/ug1708/workspace/wyj/A.UGTdatabase/pipeline_test/Bitacora_scripts

#specified species name
YourSpeices=$1

#prepare working dic
mkdir -p $YourSpeices

# (Default) GEMOMA=T (with upper case) will use GeMoMa software to predict novel genes from TBLASTN alignments (PATH to jar file need to be specified in GEMOMAP variable) 
# Otherwise, set GEMOMA=F to predict new genes by exon proximity (close-proximity method)
GEMOMA=F

# download GFF and Fasta files from NCBI and rename it in YourSpeices.fasta and YourSpeices.gff
# specified path to two files 
GenomeFile=$2
AnnoFile=$3

awk '{print$1}' $GenomeFile > ${YourSpeices}/${YourSpeices}.rename.fa
cp $AnnoFile ${YourSpeices}
perl ${PerlLib}/gff_filter_longest.pl $AnnoFile ${YourSpeices}/longestID ${YourSpeices}/${YourSpeices}.longest.gff3

# reformat GFF and call pep file 
perl ${PerlLib}/reformat_gff.pl ${YourSpeices}/${YourSpeices}.longest.gff3
perl ${PerlLib}/gff2fasta_v3.pl ${YourSpeices}/${YourSpeices}.rename.fa ${YourSpeices}/${YourSpeices}.longest.gff3_reformatted.gff3 ${YourSpeices}/${YourSpeices} 

# now run BITACORA

VERSION=1.4

SCRIPTDIR=/home/ug1708/software/bitacora-master/Scripts

GEMOMAP=/home/ug1708/miniconda3/envs/bitacora/bin/GeMoMa

NAME=${YourSpeices}

GENOME=${YourSpeices}.rename.fa

GFFFILE=${YourSpeices}.longest.gff3_reformatted.gff3

PROTFILE=${YourSpeices}.pep.fasta


##########################################################
##                 EDITABLE PARAMETERS                  ##
##########################################################

# Set CLEAN=T if you want to clean the output folder. Intermediate files will not be erased but saved in the Intermediate_files folder. Otherwise, set CLEAN=F to keep all files in the same output folder
CLEAN=T

# You can modify the E-value used to filter BLAST and HMMER. Default is 1e-5
EVALUE=1e-3

# Number of threads to be used in blast searches
THREADS=10

# (Used when GEMOMA=F; close-proximity method) Maximum length of an intron used to join putative exons of a gene. Default value is conservative and can also join exons from different genes (labeled in output files with _Ndom) 
# The provided script in Scripts/Tools/get_intron_size_fromgff.pl can estimate intron length statistics for a specific GFF. See the manual for more details
MAXINTRON=15000

# Set GENOMICBLASTP=T in order to conduct both BLASTP and HMMER to curate novel annotated genes (Note that this option is the most sensitive but greatly depends on the database quality and could result in false positives) 
# Otherwise, BITACORA will only use the protein domain (HMMER) to validate new annotated genes (In this case, the probability of detecting all copies is lower, but it will avoid to identify unrelated genes)
GENOMICBLASTP=F

# An additional validation and filtering of the resulting annotations can be conducted using the option ADDFILTER. 
# If ADDFILTER=T, BITACORA will cluster highly similar sequences (with 98% identity; being isoforms or resulting from putative assembly artifacts), and will discard all annotations with a length lower than the specified in FILTERLENGTH parameter.
ADDFILTER=T
FILTERLENGTH=100

# Alternatively, BITACORA can report all annotated genes, without any clustering of identical copies. Set RETAINNONFILTER=T in this case. 
RETAINNONFILTER=F


##########################################################
##                      HOW TO RUN                      ##
##########################################################

# Once you have included all of the above variables, you can run BITACORA as in:
#$ bash runBITACORA.sh


##########################################################
##                   PIPELINE - CODE                    ##
##########################################################

cd ${YourSpeices}

echo -e "\n#######################  Running BITACORA  #######################";
echo "BITACORA version $VERSION";
date

# Checking if provided data is ok

if [[ ! -f $SCRIPTDIR/check_data.pl ]] ; then
	echo -e "BITACORA can't find Scripts folder in $SCRIPTDIR. Be sure to add also Scripts at the end of the path as /path/Scripts";
	echo -e "BITACORA died with error\n";
	exit 1;
fi

if [ $GEMOMA == "T" ] ; then
	perl $SCRIPTDIR/check_data.pl $GFFFILE $GENOME $PROTFILE $QUERYDIR $GEMOMA $GEMOMAP 2>BITACORAstd.err
fi

if [ $GEMOMA != "T" ] ; then
	perl $SCRIPTDIR/check_data.pl $GFFFILE $GENOME $PROTFILE $QUERYDIR $GEMOMA 2>BITACORAstd.err
fi

ERRORCHECK="$(grep -c 'ERROR' BITACORAstd.err)"

if [ $ERRORCHECK != 0 ]; then
	cat BITACORAstd.err;
	echo -e "BITACORA died with error\n";
	exit 1;
fi


# Run step 1

perl $SCRIPTDIR/runanalysis.pl $NAME $PROTFILE $QUERYDIR $GFFFILE $GENOME $EVALUE $THREADS 2>>BITACORAstd.err

ERRORCHECK="$(grep -c 'ERROR' BITACORAstd.err)"

if [ $ERRORCHECK != 0 ]; then
	cat BITACORAstd.err;
	echo -e "BITACORA died with error\n";
	exit 1;
fi


# Run step 2

if [ $GEMOMA == "T" ] ; then
	if [ $GENOMICBLASTP == "T" ] ; then
		perl $SCRIPTDIR/runanalysis_2ndround_v2_genomic_withgff_gemoma.pl $NAME $PROTFILE $QUERYDIR $GENOME $GFFFILE $EVALUE $MAXINTRON $THREADS $GEMOMAP 2>>BITACORAstd.err 2>BITACORAstd.err
	fi

	if [ $GENOMICBLASTP != "T" ] ; then
		perl $SCRIPTDIR/runanalysis_2ndround_genomic_withgff_gemoma.pl $NAME $PROTFILE $QUERYDIR $GENOME $GFFFILE $EVALUE $MAXINTRON $THREADS $GEMOMAP 2>>BITACORAstd.err 2>BITACORAstd.err
	fi
fi

if [ $GEMOMA != "T" ] ; then
	if [ $GENOMICBLASTP == "T" ] ; then
		perl $SCRIPTDIR/runanalysis_2ndround_v2_genomic_withgff.pl $NAME $PROTFILE $QUERYDIR $GENOME $GFFFILE $EVALUE $MAXINTRON $THREADS 2>>BITACORAstd.err 2>BITACORAstd.err
	fi

	if [ $GENOMICBLASTP != "T" ] ; then
		perl $SCRIPTDIR/runanalysis_2ndround_genomic_withgff.pl $NAME $PROTFILE $QUERYDIR $GENOME $GFFFILE $EVALUE $MAXINTRON $THREADS 2>>BITACORAstd.err 2>BITACORAstd.err
	fi
fi

ERRORCHECK="$(grep -c 'ERROR' BITACORAstd.err)"

if [ $ERRORCHECK != 0 ]; then
	cat BITACORAstd.err;
	echo -e "BITACORA died with error\n";
	exit 1;
fi

ERRORCHECK="$(grep -c 'Segmentation' BITACORAstd.err)"

if [ $ERRORCHECK != 0 ]; then
	cat BITACORAstd.err;
	echo -e "BITACORA died with error\n";
	exit 1;
fi


# Run additional filtering and clustering
	
if [ $ADDFILTER == "T" ] ; then
	perl $SCRIPTDIR/runfiltering.pl $NAME $QUERYDIR $FILTERLENGTH 2>>BITACORAstd.err 2>BITACORAstd.err
fi

ERRORCHECK="$(grep -c 'ERROR' BITACORAstd.err)"

if [ $ERRORCHECK != 0 ]; then
	cat BITACORAstd.err;
	echo -e "BITACORA died with error\n";
	exit 1;
fi


# Cleaning 

if [ $RETAINNONFILTER == "T" ]; then
	perl $SCRIPTDIR/runcleaning_allcopies.pl $NAME $QUERYDIR
	echo -e "Cleaning output folders\n";
fi

if [ $RETAINNONFILTER != "T" ]; then
	if [ $CLEAN == "T" ]; then
	perl $SCRIPTDIR/runcleaning.pl $NAME $QUERYDIR
	echo -e "Cleaning output folders\n";
	fi
fi


rm BITACORAstd.err

echo -e "BITACORA completed without errors :)";
date

cd ..
