#!/bin/bash -x

usage() {
	echo "Usage"
	echo "usage: $0 -i genome.fa -a annoation.gff3 -s species_name -t path_to_iTools/ -c path_to_scripts/"

	echo "THIS script is used for getting input files (such as pep and cds) to Orthofinder pipeline."
	echo "YOU SHOULD install "seqtk" before use"

	echo "	Options:"
	echo "	-h	Show help message"
	echo "	-g	genome file"
	echo "	-a	filter annoation file"
	echo "	-s	species name"
	echo "	-t	path to iTools"
	echo "	-c	path to scripts"
}

while getopts "h:g:a:s:t:c:" OPT

do
	case $OPT in
		h)
			usage && exit 1
		;;
		g)

			genome="$OPTARG"
		;;
		a)
			anno="$OPTARG"
		;;
		s)
			sp_name="$OPTARG"
		;;
		t)
			iTools="$OPTARG"
		;;
		c)
			script="$OPTARG"
	esac
done

if [[ -z $genome ]] || [[ -z $anno ]] || [[ -z $sp_name ]] || [[ -z $iTools ]] || [[ -z $script ]];
then
	usage && exit 1
else 

awk '{print$1}' $genome > ${sp_name}.rename.fa

$iTools/iTools Fatools getCdsPep -Ref ${sp_name}.rename.fa -Gff $anno -OutPut $sp_name

perl $script/gff_filter_longest.pl $anno ${sp_name}_gene_mrna_cds.ids ${sp_name}.final.gff

gzip -d -f ${sp_name}.pep.fa.gz && gzip -d -f ${sp_name}.cds.fa.gz

awk '{print $2}' ${sp_name}_gene_mrna_cds.ids > ${sp_name}_mRNA.id

seqtk subseq ${sp_name}.cds.fa ${sp_name}_mRNA.id > ${sp_name}.L.cds.fa
seqtk subseq ${sp_name}.pep.fa ${sp_name}_mRNA.id > ${sp_name}.L.pep.fa

perl $script/PEP_CDS_Flt.pl ${sp_name}.L.cds.fa ${sp_name}.L.pep.fa 

sed "s/^>/>${sp_name}|/g" ${sp_name}.L.cds.fa.flt > ${sp_name}.cds.clean.fa
sed "s/^>/>${sp_name}|/g" ${sp_name}.L.pep.fa.flt > ${sp_name}.pep.clean.fa

rm ${sp_name}.L.cds.fa ${sp_name}.L.cds.fa.flt ${sp_name}.L.pep.fa ${sp_name}.L.pep.fa.flt ${sp_name}_mRNA.id  ${sp_name}_gene_mrna_cds.ids 
fi
