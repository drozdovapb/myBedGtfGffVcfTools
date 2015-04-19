This repo contains code for manipulating annotation files.

##The repository structure

The temp/ folder contains some code which is never guaranteed to work.
The scripts outside this folder should work.
The test/ folder contains examples to check the scripts.

Each commit should be marked with either 'maintenance' or 'review'.

##Meaning and intended purpose of the scripts

compare_vcf.py serves for the purpose of comparing two non-reference samples by their difference from reference. It outputs the variations from reference existing in the first of the samples (not the symmetric difference). It could be useful for comparing two samples one of which is derived from the other.
Usage: compare_vcf.py \<initial.vcf\> \<derived.vcf\> \<output.vcf\>

lexicoSV.py takes a bed file with reference-assisted annotation as input and returns the list of contigs where it finds genes from different chromosomes (could be due to structural variation or assembly errors).
It is written for S. cerevisiae standard ORF names (SGD). 
Usage: lexicoSV.py \<input.bed\> \<output.txt\>