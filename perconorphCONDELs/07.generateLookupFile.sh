gene=$1
ref_tbl=$2

outpath=orthoChainLookupFiles/$gene

grep $gene $ref_tbl | awk -F"\t" 'OFS="\t" {print $1, $2, $3}' > $outpath
results=$(grep "$gene" *reformattedChainIds)

if [ -n "${results}" ]
then
	echo "$results" | cut -d" " -f2 | sort -u >> $outpath
fi
