#!/usr/bin/perl

##############################################################################################
#
# this script is used to take chromosome start-end posistion and output corresponding sequence
#
# input file should have the following format (tab saperated)
#
# chr1   start   end   strand
# chr2   start   end   strand
#
##############################################################################################

print "command line example: perl position2sequence.pl hg18 input_file output_file\n";

if ($#ARGV ne 2) {
  print "please read the command line example\n";
  exit;
}

$ref = $ARGV[0];
$infile = $ARGV[1];
$outfile = $ARGV[2];

$ref_directory = "/home/fangjingwen/anno/$ref";

open (in, "<$infile");
open (out, ">$outfile");

while ($line=<in>) {
  if (!(($line=~/start/) or ($line=~/end/))) {
    chomp $line;
    $line=~s/\s+/\t/g;
    ($chr, $start, $end, $strand, $gene) = split /\t+/, $line;
    
    $start = $start - 1;
    $end = $end - 1;
    $length = $end - $start + 1;
    
    #  print "$chr\t$start\t$end\n";

    if (!$opened{$chr}) {
      open (fa, "<$ref_directory/$chr.fa");
      $opened{$chr} = 1;
      my @lines = <fa>;
      shift @lines;
      $seq_chr{$chr} = join "", @lines;
      $seq_chr{$chr} =~ s/\n//g;
      close fa;
    }
  
    $seq_ori = substr($seq_chr{$chr}, $start, $length);
    $seq_ori = uc($seq_ori);

    if ($strand eq "-") {
      $revcom = reverse $seq_ori;
      $revcom =~ tr/ACGTacgt/TGCAtgca/;
      $seq_ori = $revcom;
    }

    $rows = int($length/50);
    
    $start = $start + 1;
    $end = $end + 1;
    print out ">$ref\_$chr\:$start\-$end\n";
    
    for ($i=0; $i<=$rows; $i++) {
      $start = $i*50;
      $sub_seq_ori = substr ($seq_ori, $start, 50);
      print out "$sub_seq_ori\n";
    }
  }
}

close in;
close out;

