#!/bin/bash -e
set -beEu -o pipefail

tmp_dir=$1
qury_name=$2
ref_name=$3
qury_gap=$4
qury_size=$5
qury_chain=$6

if [ ! -d "$tmp_dir" ]; then
    mkdir "$tmp_dir"
fi


if [ ! -d "DELs/${qury_name}" ] ; then
	mkdir -p DELs/${qury_name}
fi

slopBed -i $qury_gap -g $qury_size -b 100 > ${tmp_dir}/${qury_name}.100bpPaddedGapTrack

python3 08-1.findDels.py $qury_chain ${tmp_dir}/${qury_name}.delsRelTo.Spodoptera_litura.unfiltered.bed ${qury_name}

subtractBed -a ${tmp_dir}/${qury_name}.delsRelTo.Spodoptera_litura.unfiltered.bed -b ${tmp_dir}/${qury_name}.100bpPaddedGapTrack > ${tmp_dir}/${qury_name}.delsRelTo.Spodoptera_litura.paddedGapSubtracted.bed

python3 08-2.switchCoords.py ${tmp_dir}/${qury_name}.delsRelTo.Spodoptera_litura.paddedGapSubtracted.bed ${tmp_dir}/${qury_name}.delsRelTo.{$ref_name}.paddedGapSubtractedCoordsSwitched.bed

sort -k4,4 ${tmp_dir}/${qury_name}.delsRelTo.{$ref_name}.paddedGapSubtractedCoordsSwitched.bed > ${tmp_dir}/${qury_name}.delsRelTo.${ref_name}.paddedGapSubtractedSortedByChain.bed

cut -f4 ${tmp_dir}/${qury_name}.delsRelTo.${ref_name}.paddedGapSubtractedSortedByChain.bed | awk -F"_" '{print $1 "_" $2 "_" $3 "_"}' | sort -u > ${tmp_dir}/listOfChainIDs

cat ${tmp_dir}/listOfChainIDs | while read currChain ; do
	grep $currChain ${tmp_dir}/${qury_name}.delsRelTo.${ref_name}.paddedGapSubtractedSortedByChain.bed | sort -u | sort -k1,1 -k2,2n > ${tmp_dir}/${currChain}.bed
	mv ${tmp_dir}/${currChain}.bed DELs/${qury_name}/${currChain}.bed
done

rm -r ${tmp_dir}

