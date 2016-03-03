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


def correct_coord(gff, out_filename):
    """
    This function takes a gtf2 file (gtf2_filename),
    writes a gff3 file to gff3_filename
    and also returns a list of lists
    Optimized for feeding ProteinOrtho
    """
    cnt = 0
    for line in gff:
        if line[3] > line[4]:
            line[4], line[3] = line[3], line[4]
            cnt += 1
    io.write_tsv(gff, out_filename)
    print("corrected ", str(cnt), "lines")
    return gff


def main():
    """
    Inputs: input file, output file, conversion function, other arguments
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_filename", help="input file to work with", required=True)
    parser.add_argument("-o", "--out", default="corrected.gff", help="output gff file")

    args = parser.parse_args()

    input_list_of_lists = io.read_tsv(args.input_filename)

    correct_coord(input_list_of_lists, args.out)


if __name__ == "__main__":
    main()
