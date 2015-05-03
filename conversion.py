#!/usr/bin/env python3

import sys
import itertools
#import pysed
import re


def read_tsv(filename):
    """
    Basically, all flavors of gff and gtf as well as vcf and bed files
    are just tab separated tables
    """
    with open(filename, 'r') as fh:
        return [line.split('\t') for line in fh]


def write_tsv(list_obj, output_file):
    with open(output_file, 'w') as out:
        for line in list_obj:
            out.write('\t'.join(line))
            #out.write('something')


def gtf2gff3(gtf2_filename, gff3_filename, CDS_only = True):
    """
    :param gtf2_filename:
    :return:
    Once fed up
    Useful for feeding ProteinOrtho ;)
    CDS only here is the default option
    """
    gtf2 = read_tsv(gtf2_filename)
    gff3 = []
    with open(gff3_filename, 'w') as out:
        for line in gtf2:
            #print(line[-1])  # line[8] doesn't work for some strange reason but line[-1] does
            #print(line[2:3])  # line[2:3] works but line[2] does not
            if CDS_only:
                if line[2:3] == ['CDS']:
                    line[-1] = re.sub(r'gene_id \"(E\w*).*$', 'ID=\g<1>;', line[-1])
                    gff3.append(line)
                    out.write('\t'.join(line))
            else:
                line[-1] = re.sub(r'gene_id \"(E\w*).*$', 'ID=\g<1>;', line[-1])
                gff3.append(line)
                out.write('\t'.join(line))
    return gff3


def gff32gtf(gff3):
    """
    :param gff3:
    :return:
    """
    pass


def gff32bed(gff3):
    """
    All ***2bed functions are utterly useful for working with the UCSC genome browser
    :param gff3:
    :return:
    """
    pass


def bed2gff(bedfile_name):
    """
    The idea taken from galaxy
    :param bed:
    :return:
    """
    bed = read_tsv(bedfile_name)
    gff = []
    i = 0
    for i, line in enumerate(bed):
        complete_bed = False
        line = line.rstrip( '\r\n' )
        if line and not line.startswith( '#' ) and not line.startswith( 'track' ) and not line.startswith( 'browser' ):
            try:
                elems = line.split( '\t' )
                if len( elems ) == 12:
                    complete_bed = True
                chrom = elems[0]
                if complete_bed:
                    feature = "gene"
                else:
                    try:
                        feature = elems[3]
                    except:
                        feature = 'feature%d' % ( i + 1 )
                start = int( elems[1] ) + 1
                end = int(elems[2])
                score = elems[4]
                strand = elems[5]
                group = 'gene_id ' + '"' + elems[3] + '"' + '; transcript_id ' + '"' + elems[3] + '"' + '; gene_biotype "protein_coding"'

                if complete_bed:
                    gff.append('\t'.join([chrom, 'bed2gff', feature, start, end, score, strand, feature, group]))
                    gff.append('\t'.join([chrom, 'protein_coding', feature, start, end, score, strand, feature, group]))
                else:
                    gff.append('\t'.join([chrom, 'protein_coding', feature, start, end, score, strand,'.', group]))
                if complete_bed:
                    # We have all the info necessary to annotate exons for genes and mRNAs

                    block_count = int( elems[9] )
                    block_sizes = elems[10].split( ',' )
                    block_starts = elems[11].split( ',' )
                    for j in range( block_count ):
                        exon_start = int( start ) + int( block_starts[j] )
                        exon_end = exon_start + int( block_sizes[j] ) - 1

                        #first exons

                        if j == 0:
                            frame = 0

                        #Here really should be some code to deal with introns


                        else:
                            frame = 0


                        out.write( '%s\tprotein_coding\tCDS\t%d\t%d\t%s\t%s\t%s\texon %s;\n'
                                   % ( chrom, exon_start, exon_end, score, strand, frame, group ) )
                        #out.write( '%s\tprotein_coding\tmRNA\t%d\t%d\t%s\t%s\t%d\tCDS %s;\n' % ( chrom, exon_start, exon_end, score, strand, frame, group ) )
            except:
                skipped_lines += 1
                if not first_skipped_line:
                    first_skipped_line = i + 1
        else:
            skipped_lines += 1
            if not first_skipped_line:
                first_skipped_line = i + 1
    out.close()
    info_msg = "%i lines converted to GFF version 2.  " % ( i + 1 - skipped_lines )
    if skipped_lines > 0:
        info_msg += "Skipped %d blank/comment/invalid lines starting with line #%d." %( skipped_lines, first_skipped_line )
    print(info_msg)

if __name__ == "__main__": __main__()
