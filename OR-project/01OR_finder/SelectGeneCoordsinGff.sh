spname=$1
gff=$2
outfile=$3
round=$4

filename="$spname.b.filter.$round.id"

cat $filename | cut -f 1 | while read a 
do
	grep ${a} $gff | awk '$3=="mRNA"{print$1"\t"$4"\t"$5}' >> $outfile
done
