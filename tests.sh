#! /bin/bash

echo -e 'conversion.py without parameters'
./conversion.py
echo -e 'conversion.py help'
./conversion.py -h 
echo -e 'all conversion functions (look at the output)'
./conversion.py -f bed_to_gff3 -i test/test_liftover.bed -o ../test_bed.gff
./conversion.py -f gff_to_bed -i test/test_augustus_gff3.gff -o ../test_gff.bed
./conversion.py -f gtf_to_gff3 -i test/test_gm_es.gtf -o ../test_gtf.gff3

echo -e 'checking line count'
wc -l test/test_liftover.bed
wc -l ../test_bed.gff
wc -l test/test_augustus_gff3.gff
echo 'grep -cv \#'
grep -cv \# test/test_augustus_gff3.gff
wc -l ../test_gff.bed
wc -l test/test_gm_es.gtf 
wc -l ../test_gtf.gff3

