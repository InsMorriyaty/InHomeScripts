#Fliter by: 
#1) The protein seq less than 50aa;
#2) The pep unmatch with cds;
#3) The pep Seq with internal Stop codon;
#4) The pep Seq with invalid character;
use warnings;
use strict;
use Bio::SeqIO;

my $cds=shift or die "perl $0 cds pep\n";
my $pep=shift or die "perl $0 cds pep\n";

my @seq=($cds,$pep);
my %seq;

for my $file(@seq){
    my $type;
    my $fa=Bio::SeqIO->new(-file=>$file,-format=>'fasta');
    if ($file=~/cds/i){
	$type="cds";
    }else{
	$type="pep";
    }
    while(my $seq_obj=$fa->next_seq){
	my $id=$seq_obj->id;
	my $seq=$seq_obj->seq;
	$seq{$id}{$type}=$seq;
	
    }
}

my $a=0;
open(C,">$cds.flt");
open(P,">$pep.flt");
foreach my $id (keys %seq){#print "$id\n";exit;
    if(exists $seq{$id}{pep} and $seq{$id}{cds}){
	$seq{$id}{pep}=~s/\*$//;
	next if $seq{$id}{pep}=~/\*/;
	next if ($seq{$id}{pep}=~/^X/ and $seq{$id}{pep}=~/X$/);
	my $len=length $seq{$id}{pep};
	next if $len<50;
	my $trans=&TranslateDNASeq($seq{$id}{cds});
	$trans=~s/\*$//;#print "$id\n$trans\n";exit;
	if ($trans ne $seq{$id}{pep}){
	    $a++;
	}else{
	    print C ">$id\n$seq{$id}{cds}\n";
	    print P ">$id\n$seq{$id}{pep}\n";
	}
    }
}#print "$a\n";
close C;
close P;

sub TranslateDNASeq(){
    use Bio::Seq;
    (my $dna)=@_;
    my $seqobj=Bio::Seq->new(-seq =>$dna, -alphabet =>'dna');
    return $seqobj->translate()->seq(); # if the codetable is mit of vertebrate you should replace translate() to translate (-codontable_id => 2); invertebrate mito 5
}
