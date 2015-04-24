##Annotation file formats

GFF2 has nine required fields (seqname, source, feature, start, end, score, strand, frame, group).
See more at https://genome.ucsc.edu/FAQ/FAQformat.html#format3

GTF2.2 is alike GFF2 but more strictly defined. Eight required fields + the 'group' feature expanded into attributes + comments:
<seqname> <source> <feature> <start> <end> <score> <strand> <frame> [attributes] [comments]
Attributes must contain transcript_id / protein_id / gene_id
See more at (http://mblab.wustl.edu/GTF2.html)

GFF3 is the newer version of GFF not supported by some browsers.


VCF is designed to store information about sequence variations. 
CHROM POS ID REF ALT QUAL FILTER INFO FORMAT <sample1> <...>
VCF4.1 and VCF4.2 differ mostly in the INFO field.
http://samtools.github.io/hts-specs/VCFv4.1.pdf
http://samtools.github.io/hts-specs/VCFv4.2.pdf

BED is the most flexible of these formats. It can store anything and has only 3 required fields (+ 9 additional fields):
chrom, chromStart, chromEnd, 
name, score, strand, thickStart, thickEnd, itemRgb, blockCount, blockSizes, blockStarts
See more at https://genome.ucsc.edu/FAQ/FAQformat.html#format1