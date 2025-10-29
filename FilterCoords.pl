#!/usr/bin/perl -w
use strict;
die  "Version 1.0\t2021-01-11;\nUsage: $0 <InPut>\n" unless (@ARGV ==1);
open (IA,"$ARGV[0]") || die "input file can't open $!";
<IA>;<IA>;<IA>;<IA>;<IA>;
        while(<IA>)
        {
                chomp ;
                my @inf=split ;
                next if  ($inf[6]<90);
                print "$inf[-2]\t$inf[0]\t$inf[1]\t$inf[-2]\t$inf[-1]\t$inf[3]\t$inf[4]\n";
        }
close IA;
