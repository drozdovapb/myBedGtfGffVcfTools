##Annotation file formats

GFF2 has nine required fields (seqname, source, feature, start, end, score, strand, frame, group).
See more at https://genome.ucsc.edu/FAQ/FAQformat.html#format3

GTF2.2 is alike GFF2 but more strictly defined. Eight required fields + the 'group' feature expanded into attributes + comments:
<seqname> <source> <feature> <start> <end> <score> <strand> <frame> [attributes] [comments]
Attributes must contain transcript_id / protein_id / gene_id
See more at (http://mblab.wustl.edu/GTF2.html)
Biomart example:
1	ensembl	gene	11193	15975	.	+	.	gene_id "ENSECAG00000012421"; gene_version "1"; gene_name "SYCE1"; gene_source "ensembl"; gene_biotype "protein_coding";


GFF3 is the newer version of GFF not supported by some browsers.
Different versions
poff preferred example:
gi<something>	sim	CDS	1	1	.	+	.	ID=C_1;
Specification here: http://gmod.org/wiki/GFF3#GFF3_Format
seqid, source, type, start, end, score, strand, phase, attributes
attributes: ID, Name, Alias, Parent, Target, Gap, Derives_from, Note, Dbxref, Ontology term.


VCF is designed to store information about sequence variations. 
CHROM POS ID REF ALT QUAL FILTER INFO FORMAT <sample1> <...>
VCF4.1 and VCF4.2 differ mostly in the INFO field.
http://samtools.github.io/hts-specs/VCFv4.1.pdf
http://samtools.github.io/hts-specs/VCFv4.2.pdf

BED is the most flexible of these formats. It can store anything and has only 3 required fields (+ 9 additional fields):
chrom, chromStart, chromEnd, 
name, score, strand, thickStart, thickEnd, itemRgb, blockCount, blockSizes, blockStarts
See more at https://genome.ucsc.edu/FAQ/FAQformat.html#format1