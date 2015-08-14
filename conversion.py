#!/usr/bin/env python3

import re
import argparse
import io_tools as io


def _id_gff2_to_gff3(attributes):
    # change and save gene_id
    attributes = re.sub(r'gene_id \"(\w*).*?"', 'ID=\g<1>', attributes)
    # change and save gene_name
    attributes = re.sub(r'gene_name \"(\w*).*?"', 'Name=\g<1>', attributes)
    # get rid of other details
    attributes = re.sub(r'gene_.*? \"(\w*).*?\";', '', attributes)
    return attributes


def gtf_to_gff3(gtf2, gff3_filename, cds_only=False):
    """
    This function takes a gtf2 file (gtf2_filename),
    writes a gff3 file to gff3_filename
    and also returns a list of lists
    Optimized for feeding ProteinOrtho
    """
    gff3 = []
    for line in gtf2:
        if cds_only:
            if line[2] == 'CDS':
                line[-1] = _id_gff2_to_gff3(line[-1])
                gff3.append(line)
        else:
            line[-1] = _id_gff2_to_gff3(line[-1])
            gff3.append(line)
    io.write_tsv(gff3, gff3_filename)
    return gff3


def gff3_to_gtf(gff3):
    """
    :param gff3:
    :return:
    """
    pass


def gff_to_bed(gff3, bed_filename):
    """
    All ***2bed functions are utterly useful for working with the UCSC genome browser
    This function takes a gtf/gff-like object or reads a file,
     writes a bed file and also returns a bed-like object
    This version supports short bed files only
    Future versions will support long bed files (12 fields)
    """
    bed = []
    for line in gff3:
        #bed used 0-based coordinates while gff uses 1-based coordinates
        chrom = line[0]
        start, stop = str(int(line[3])-1), line[4]
        #name = line[8][3:9]  # change this to something more flexible!!!!
        name = line[8][3:]
        score, strand = line[5], line[6]
        bed.append([chrom, start, stop, name, score, strand])
    io.write_tsv(bed, bed_filename)
    return bed


def bed_to_gff3(bed, gff_filename, source='bed2gff'):
    """
    The idea is taken from galaxy (usegalaxy.org) but was sufficiently renewed
    This function takes a bed file,
    writes a gff3 file and also returns a gff3-like object
    Source may be explicitly specified by the user (eg the program used to obtain evidence)
    """
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
    io.write_tsv(gff, gff_filename)
    return gff


def main():
    """
    Inputs: input file, output file, conversion function, other arguments
    """

    parser = argparse.ArgumentParser()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-f", "--function", help="function name "
                                                   "(currently implemented functions: "
                                                   "\n gtf_to_gff3, gff_to_bed, bed_to_gff3)", required=True)
    required.add_argument("-i", "--input_filename", help="input file to work with", required=True)
    required.add_argument("-o", "--output_filename", help="output file to write to", required=True)

    parser.add_argument("--source", default="bed2gff", help="source information in gtf "
                                                            "(program that generated this file,"
                                                            "database or project name)")
    parser.add_argument("--cds_only", type=bool, default=False, help="generate only CDS lines"
                                                                     "(default is FALSE)")

    args = parser.parse_args()

    input_list_of_lists = io.read_tsv(args.input_filename)

    if args.function == 'gtf_to_gff3':
        gtf_to_gff3(input_list_of_lists, args.output_filename, args.cds_only)
    elif args.function == "gff_to_bed":
        gff_to_bed(input_list_of_lists, args.output_filename)
    elif args.function == "bed_to_gff3":
        bed_to_gff3(input_list_of_lists, args.output_filename, args.source)
    else:
        print(args.function, ': This function is not implemented')
        print("Currently implemented functions: gtf_to_gff3, gff_to_bed, bed_to_gff3")

if __name__ == "__main__":
    main()
