use strict;
use warnings;

## created by Yongzhi Yang. 2017/3/20 ##

#my $mafft="/home/data_disk_38T/luzhiqiang_work/software/mafft/mafft-7.429-without-extensions-build/bin/mafft";
my $mafft="mafft";
my $pal2nal="pal2nal.pl";

my @in=<align/*/pep>;
for my $in (@in){
    my $in2=$in;
    $in2=~s/pep/cds/;
    print "$mafft --auto $in > $in.best.fas ; $pal2nal $in.best.fas $in2 -output fasta > $in2.best.fas ; trimal -in $in2.best.fas -out $in2.best.fas.trim -automated1 \n";
}
