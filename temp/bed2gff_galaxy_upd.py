#!/usr/bin/env python

# This code

import sys

assert sys.version_info[:2] >= ( 2, 4 )

def __main__():
    input_name = sys.argv[1]
    #chr_sizes = sys.argv[2]
    output_name = sys.argv[2]
    skipped_lines = 0
    first_skipped_line = 0
    out = open( output_name, 'w' )
    out.write( "##gff-version 2\n" )
    out.write( "##bed_to_gff_converter.py\n\n" )


    #chr sizes
#    sizes = dict()
#    with open(chr_sizes, 'r') as chrsizes:
#        for line in chrsizes:
#            sizes[line.split('\t')[0]] = int(line.split('\t')[1])
            #print(line)


    i = 0
    for i, line in enumerate( file( input_name ) ):
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
                end = int( elems[2] )
                try:
                    score = elems[4]
                except:
                    score = '0'
                try:
                    strand = elems[5]
                except:
                    strand = '+'
#                try:
                group = 'gene_id ' + '"' + elems[3] + '"' + '; transcript_id ' + '"' + elems[3] + '"' + '; gene_biotype "protein_coding"'
#                except:
#                    group = 'group%d' % ( i + 1 )
                if complete_bed:
                    out.write( '%s\tbed2gff\t%s\t%d\t%d\t%s\t%s\t.\t%s %s;\n' % ( chrom, feature, start, end, score, strand, feature, group  ) )
                    out.write( '%s\tprotein_coding\t%s\t%d\t%d\t%s\t%s\t.\t%s %s;\n' % ( chrom, feature, start, end, score, strand, feature, group  ) )
                else:
                    out.write( '%s\tprotein_coding\t%s\t%d\t%d\t%s\t%s\t.\t%s;\n' % ( chrom, feature, start, end, score, strand, group  ) )
                if complete_bed:
                    # We have all the info necessary to annotate exons for genes and mRNAs

                    block_count = int( elems[9] )
                    block_sizes = elems[10].split( ',' )
                    block_starts = elems[11].split( ',' )
                    for j in range( block_count ):
                        exon_start = int( start ) + int( block_starts[j] )
                        exon_end = exon_start + int( block_sizes[j] ) - 1


#                            #frames!!!
#                        if strand == '+':
#                            frame = exon_start % 3
#                        elif strand == '-':
#                            frame = sizes[chrom] % 3
#                            frame = (sizes[chrom] - exon_start) % 3
#                        else:
#                            frame = 'wtf'

                    #we assume that we have only full genes

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
    print info_msg

if __name__ == "__main__": __main__()
