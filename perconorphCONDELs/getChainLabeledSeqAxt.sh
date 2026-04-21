#!/bin/bash -e

set -beEu -o pipefail

qury=$1
ref=$2
orthochain=$3
chainid=$4

if [ ! -d "labeledAxts/${ref}.${qury}chainLabeled.axts" ] ; then
        mkdir -p labeledAxts/${ref}.${qury}chainLabeled.axts
fi

for chainID in $(cut -f2 ${chainid} | sort -u); do
	cat ${orthochain} | chainFilter -id=${chainID} stdin | chainToAxt stdin ${ref}.2bit ${qury}.2bit stdout | awk -v descriptor=${qury}_chain${chainID}_ '{if ($1 ~ /[0-9]/) $0 = $0 " " descriptor; print $0 }' > labeledAxts/${ref}.${qury}chainLabeled.axts/${qury}_chain${chainID}_.axt
done
