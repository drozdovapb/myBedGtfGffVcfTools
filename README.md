This repo contains code for manipulating annotation file formats.

##Repository structure

The `temp/` folder contains some code which is never guaranteed to work.

The scripts outside this folder should work.

The `test/` folder contains examples to check the scripts.

##Meaning and intended purpose of the scripts

**compare_vcf.py** serves for the purpose of comparing two non-reference samples by their difference from reference. It outputs the variations from reference existing in the first of the samples (not the symmetric difference). It could be useful for comparing two samples one of which is derived from the other.

Usage: `compare_vcf.py <initial.vcf> <derived.vcf> <output.vcf>`

update: it does work but bedtools intersect -v is much faster, so I would strongly recommend using this well-known tool instead of my code.

**correct_coord.py** <input.gff/bed> <output.gff/bed>

Some programs (e.g. command line Blast tabular output) list coordinates of the features as the find them, and so start can happen to be greater than stop. 
Such data cannot be directly used as input to bedtools. This script solves this problem.

**lexicoSV.py** takes a bed file with reference-assisted annotation as input and returns the list of contigs where it finds genes from different chromosomes (could be due to structural variation or assembly errors).
It is written for S. cerevisiae standard ORF names (SGD). 

Usage: `lexicoSV.py <input.bed> <output.txt>`

**conversion.py**, the main script in this folder
Usage: `conversion.py [-h] -f FUNCTION -i INPUT_FILENAME -o OUTPUT_FILENAME
                     [--source SOURCE] [--cds_only CDS_ONLY]`
Currently supported formats: gtf to gff3, gff/gtf to bed, bed to gff3. 

**rename_gff** scripts are useful if you have some annotation in which genes are not given any proper names (e.g. Maker2 output) and some knowledge about how these features shown be named (e.g. from a related species or another subspecies / strain / cultivar etc).
**rename_gff_by_table** was written specifically for proteinortho output but should be applicable to any similar output.
proteinortho output looks like this: 
`# Species	Genes	Alg.-Conn.	<sample1 name> 	<sample2 name>`
The basic idea is to cluster sequences and use the table to rename entries.

**tests.py** and **tests.sh** are just some scripts to test the code and report where it fails.


##Annotation file formats

###GFF2

GFF2 has nine required fields. GTF2 should be identical to GFF2. 

1. [0] seqname
2. [1] source
3. [2] feature
4. [3] start
5. [4] end
6. [5] score
7. [6] strand
8. [7] frame
9. [8] group

See more at https://genome.ucsc.edu/FAQ/FAQformat.html#format3, http://www.ensembl.org/info/website/upload/gff.html, and https://www.sanger.ac.uk/resources/software/gff/spec.html


###GTF2.2

GTF2.2 is alike GFF2 but more strictly defined. Eight required fields + the 'group' feature expanded into attributes + comments:


1. [0] seqname 
2. [1] source 
2. [2] feature
4. [3] start 
5. [4] end
6. [5] score
7. [6] strand
8. [7] frame
9. [8] attributes + comments

Possible attributes: transcript_id / protein_id / gene_id

Of note: the name and the value of each attribute are separated with a space, and values are in quotes.


Biomart example:

`1	ensembl	gene	11193	15975	.	+	.	gene_id "ENSECAG00000012421"; gene_version "1"; gene_name "SYCE1"; gene_source "ensembl"; gene_biotype "protein_coding";`

See more at (http://mblab.wustl.edu/GTF2.html)


###GFF3

GFF3 is the newer version of GFF not supported by some genome browsers (e.g. the UCSC genome browser). 

1. [0] seqid
2. [1] source
3. [2] type
4. [3] start
5. [4] end
6. [5] score
7. [6] strand
8. [7] phase
9. [8] attributes

Possible attributes: ID, Name, Alias, Parent, Target, Gap, Derives_from, Note, Dbxref, Ontology term.

Of note: the name and the value of each attribute are separated with a =, and values are in plain text (no quotes).

poff preferred example:

`gi<something>	sim	CDS	1	1	.	+	.	ID=C_1;`

See more at http://gmod.org/wiki/GFF3#GFF3_Format


###VCF

VCF is designed to store information about sequence variations. 

1. [0] CHROM
2. [1] POS 
3. [2] ID 
4. [3] REF 
5. [4] ALT 
6. [5] QUAL 
7. [6] FILTER 
8. [7] INFO 
9. [8] FORMAT 
10 [9] <sample1>
...

VCF4.1 and VCF4.2 differ mostly in the INFO field.

See more at http://samtools.github.io/hts-specs/VCFv4.1.pdf and http://samtools.github.io/hts-specs/VCFv4.2.pdf

###BED

BED is the most flexible of these formats. It can store anything and has only 3 required fields + 9 additional fields:

1. [0] chrom
2. [1] chromStart
3. [2] chromEnd
4. [3] name
5. [4] score
6. [5] strand
7. [6] thickStart
8. [7] thickEnd
9. [8] itemRgb
10. [9] blockCount
11. [10] blockSizes
12. [11] blockStarts


See more at https://genome.ucsc.edu/FAQ/FAQformat.html#format1
