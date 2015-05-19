#!/usr/bin/env python3

import re
import sys
import getopt
import base_functions as bf


def _id_gff2_to_gff3(attributes):
    # change and save gene_id
    attributes = re.sub(r'gene_id \"(\w*).*?"', 'ID=\g<1>', attributes)
    # change and save gene_name
    attributes = re.sub(r'gene_name \"(\w*).*?"', 'Name=\g<1>', attributes)
    # get rid of other details
    attributes = re.sub(r'gene_.*? \"(\w*).*?\";', '', attributes)
    return attributes


def gtf2gff3(gtf2_filename, gff3_filename, cds_only=False):
    """
    This function takes a gtf2 file (gtf2_filename),
    writes a gff3 file to gff3_filename
    and also returns a list of lists
    Optimized for feeding ProteinOrtho
    """
    gtf2 = bf.read_tsv(gtf2_filename)
    gff3 = []
    for line in gtf2:
        if cds_only:
            if line[2] == ['CDS']:
                line[-1] = _id_gff2_to_gff3(line[-1])
                gff3.append(line)
        else:
            line[-1] = _id_gff2_to_gff3(line[-1])
            gff3.append(line)
    bf.write_tsv(gff3, gff3_filename)
    return gff3


def gff32gtf(gff3):
    """
    :param gff3:
    :return:
    """
    pass


def gff2bed(gff3_filename, bed_filename):
    """
    All ***2bed functions are utterly useful for working with the UCSC genome browser
    This function takes a gtf/gff-like object or reads a file,
     writes a bed file and also returns a bed-like object
    This version supports short bed files only
    Future versions will support long bed files (12 fields)
    """
    gff3 = bf.read_tsv(gff3_filename)
    bed = []
    for line in gff3:
        #bed used 0-based coords while gff uses 1-based coords
        chrom = line[0]
        start, stop = str(int(line[3])-1), line[4]
        bed.append([chrom, start, stop])
    bf.write_tsv(bed, bed_filename)
    return bed


def bed2gff3(bed_filename, gff_filename, source='bed2gff'):
    """
    The idea is taken from galaxy (usegalaxy.org) but was sufficiently renewed
    This function takes a bed file,
    writes a gff3 file and also returns a gff3-like object
    Source may be explicitly specified by the user (eg the program used to obtain evidence)
    """
    bed = bf.read_tsv(bed_filename)
    gff = []
    long_bed = len(bed[0]) == 12
    for line in bed:
        chrom = line[0]
        start = str(int(line[1]) + 1)
        end = line[2]
        # if there are only 3 fields (short bed) we do not have enough information
        score, strand, attributes = '0', '.', ''
        #bed formatted files do not store source, phase and type information. Alas
        feature_type = "gene"
        phase = '.'
        if long_bed:
            genename, score, strand = line[3:6]
            attributes = 'ID=' + genename
        gff.append([chrom, source, feature_type, start, end, score, strand, phase, attributes])
        # Some code to deal with introns will be here
    bf.write_tsv(gff, gff_filename)
    return gff


def main():
    """
    Inputs: input file, output file, conversion function, other arguments
    """
    cds_only, source = False, 'bed2gff'  # pass default argument values

    if len(sys.argv) < 5:
        # print usage message and quit
        print('conversion.py -f <function> -i <inputfile> -o <outputfile>')
        sys.exit(2)

    opts, args = getopt.getopt(sys.argv[1:], "hf:i:o:",
                                   ['help', 'function=', 'input=', 'output=', 'source=', 'cds_only'])
    for opt, arg in opts:
        if opt in ('-f', '--function'):
            function_name = arg
        elif opt in ('-i', '--input'):
            input_filename = arg
        elif opt in ('-o', '--output'):
            output_filename = arg
        elif opt in ('-h','--help'):
            print('conversion.py -f <function> -i <inputfile> -o <outputfile>')
        elif opt == 'source=':
            source = arg
        elif opt == 'cds=only':
            cds_only = arg

    if function_name == 'gtf2gff3':
        gtf2gff3(input_filename, output_filename, cds_only)
        print('sm')
    elif function_name == "gff2bed":
        gff2bed(input_filename, output_filename)
    elif function_name == "bed2gff3":
        bed2gff3(input_filename, output_filename, source)
    else:
        print('This function is not implemented')
        sys.exit(2)

if __name__ == "__main__":
    main()