#!/bin/bash


#These lines need to be modified
path= #set path to the vcf files
strain = #set sample name, e.g. 15V

cp path/$strain.eff.vcf .

#restore 'chr' in the vcf entries
sed 's/^/chr/' $strain.eff.coding.vcf >$strain.eff.coding.chr.vcf

#snpEff breaks the header
#a quick fix with the previous file (mpileup output)
grep \# path/$strain.filt.vcf >$strain.head.txt
grep -v \# $strain.eff.coding.chr.vcf >$strain.tail.txt
cat $strain.head.txt $strain.tail.txt >$strain.cont.vcf
#now we have a valid vcf4.2 file
sed 's/contig=<ID=/contig=<ID=chr/' $strain.cont.vcf >$strain.v4.2.vcf


#downgrade vcf4.2 to vcf4.1
#many thanks to http://danielecook.com/downgrade-vcf-viewing-igv-4-2-4-1/ for the idea
sed "s/##fileformat=VCFv4.2/##fileformat=VCFv4.1/" $strain.v4.2.vcf| \
  sed "s/(//" | \
  sed "s/)//" | \
  sed "s/,Version=\"3\">/>/" | \
  sed 's/\"//' >$strain.vcf  #now we have a valid vcf4.1 file

#garbage removal
rm $strain.*.txt #remove head and tail, we don't need them
rm $strain.cont.vcf #remove intermediate result
rm $strain.eff.* #remove badly formatted snpEff files and intermediate steps




