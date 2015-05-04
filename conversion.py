#!/usr/bin/env python3

import re


def read_tsv(filename):
    """
    Basically, all flavors of gff and gtf as well as vcf and bed files
    are just tab separated tables.
    This function takes a filename
    and returns a list of lists
    """
    with open(filename, 'r') as fh:
        return [line.split('\t') for line in fh]


def write_tsv(list_obj, output_file):
    """
    Takes a list of lists (list_obj) and writes a file (output_file)
    This function doesn't return anything
    """
    with open(output_file, 'w') as out:
        for line in list_obj:
            out.write('\t'.join(line))


def id_gff2_to_gff3(line):
    # change and save gene_id
    line[-1] = re.sub(r'gene_id \"(\w*).*?"', 'ID=\g<1>', line[-1])
    #change and save gene_name
    line[-1] = re.sub(r'gene_name \"(\w*).*?"', 'Name=\g<1>', line[-1])
    #get rid of other details
    re.sub(r'gene_.*? \"(\w*).*?\";', '', line[-1])


def gtf2gff3(gtf2_filename, gff3_filename, cds_only=True):
    """
    This function takes a gtf2 file (gtf2_filename),
    writes a gff3 file to gff3_fileliname
    and also returns a list of lists
    Optimized for feeding ProteinOrtho
    CDS only here is the default option, and it can be changed
    """
    gtf2 = read_tsv(gtf2_filename)
    gff3 = []
    with open(gff3_filename, 'w') as out:
        for line in gtf2:
            #print(line[-1])  # line[8] doesn't work for some strange reason but line[-1] does
            #print(line[2:3])  # line[2:3] works but line[2] does not
            if cds_only:
                if line[2:3] == ['CDS']:
                    id_gff2_to_gff3(line)
                    gff3.append(line)
            else:
                id_gff2_to_gff3(line)
                gff3.append(line)
    write_tsv(gff3, gff3_filename)
    return gff3


def gff32gtf(gff3):
    """
    :param gff3:
    :return:
    """
    pass


def gff2bed(gff3_filename, bed_filename, fromfile=True):
    """
    All ***2bed functions are utterly useful for working with the UCSC genome browser
    This function takes a gtf/gff-like object or reads a file,
     writes a bed file and also returns a bed-like object
    This version supports short bed files only
    Future versions will support long bed files (12 fields)
    """
    if fromfile:
            gff3 = read_tsv(gff3_filename)
    else:
        gff3 = gff3_filename
    bed = []
    for line in gff3:
        #bed used 0-based coords while gff uses 1-based coords
        chrom = line[0]
        start, stop = int(line[3])-1, int(line[4])
        bed.append([chrom, start, stop])
    write_tsv(bed, bed_filename)
    return bed


def bed2gff(bed_filename, out):
    """
    The idea is taken from galaxy (usegalaxy.org)
    :param bed:
    :return:
    The code below this point is not worth reading
    """
    bed = read_tsv(bed_filename)
    gff = []
    for line in bed:
        long_bed = False
        if line and not line[0].startswith('#') and not line[0].startswith('track') and not line[0].startswith('browser'):
            if len(line) == 12:
                long_bed = True
            chrom = line[0]
            if long_bed:
                feature = "gene"
            else:
                feature = line[3]
            start = int(line[1]) + 1
            end = int(line[2])
            score = line[4]
            strand = line[5]
            group = 'gene_id ' + '"' + line[3] + '"' + '; transcript_id ' + '"' + line[3] + '"' + '; gene_biotype "protein_coding"'
            if long_bed:
                gff.append('\t'.join([chrom, 'bed2gff', feature, start, end, score, strand, feature, group]))
                gff.append('\t'.join([chrom, 'protein_coding', feature, start, end, score, strand, feature, group]))
            else:
                gff.append('\t'.join([chrom, 'protein_coding', feature, start, end, score, strand,'.', group]))
            if long_bed:
                # We have all the info necessary to annotate exons for genes and mRNAs
                block_count = int( line[9] )
                block_sizes = line[10].split(',')
                block_starts = line[11].split(',')
                for j in range(block_count):
                    exon_start = int(start) + int( block_starts[j] )
                    exon_end = exon_start + int( block_sizes[j] ) - 1
                    #first exons
                    if j == 0:
                        frame = 0
                    #Here really should be some code to deal with introns
                    else:
                        frame = 0
                    out.write('%s\tprotein_coding\tCDS\t%d\t%d\t%s\t%s\t%s\texon %s;\n'
                               % (chrom, exon_start, exon_end, score, strand, frame, group))
                    out.close()



#if __name__ == "__main__": main()
