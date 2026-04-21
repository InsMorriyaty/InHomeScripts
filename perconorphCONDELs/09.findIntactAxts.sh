#!/bin/bash -e
set -beEu -o pipefail

tmp_dir=$1
qury_name=$2
ref_name=$3
ortho_chain=$4


if [ ! -d "$tmp_dir" ]; then
    mkdir "$tmp_dir"
fi


if [ ! -d "axtBlocks/${qury_name}" ] ; then
        mkdir -p axtBlocks/${qury_name}
fi

python3 09-1.findIntactRegions.py ${ortho_chain} ${tmp_dir}/${qury_name}.IntactAligmntsRelTo.${ref_name}_unsorted.bed ${qury_name}

sort -k4,4 ${tmp_dir}/${qury_name}.IntactAligmntsRelTo.${ref_name}_unsorted.bed > ${tmp_dir}/${qury_name}.IntactAligmntsRelTo.${ref_name}_sortedByChainID.bed

while [ -s ${tmp_dir}/${qury_name}.IntactAligmntsRelTo.${ref_name}_sortedByChainID.bed ]; do  # while the file still has lines
	currChain=$(head -1 ${tmp_dir}/${qury_name}.IntactAligmntsRelTo.${ref_name}_sortedByChainID.bed | cut -f4 | awk -F"_" '{print $1 "_" $2 "_" $3 "_"}')  # e.g. balAcu1_chain2049_

	# save off all entries from the current chain
	cat ${tmp_dir}/${qury_name}.IntactAligmntsRelTo.${ref_name}_sortedByChainID.bed | grep $currChain | sort -k1,1 -k2,2n > ${tmp_dir}/${currChain}.bed

	# count how many entries came from current chain
	numLines=$(wc -l ${tmp_dir}/${currChain}.bed | cut -d" " -f1)

	# move saved entries from current chain to outdir
	cat ${tmp_dir}/${currChain}.bed > axtBlocks/${qury_name}/${currChain}.bed
	rm ${tmp_dir}/${currChain}.bed

	# delete entries that have already been considered
	sed -i '1,'"$numLines"'d' ${tmp_dir}/${qury_name}.IntactAligmntsRelTo.${ref_name}_sortedByChainID.bed

done
