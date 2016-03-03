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


def correct_coord(list_of_lists, filetype, out_filename):
    """
    This function takes a gtf2 file (gtf2_filename),
    writes a gff3 file to gff3_filename
    and also returns a list of lists
    Optimized for feeding ProteinOrtho
    """
    cnt = 0
    if filetype == "bed":
        start, stop = 1, 2
    elif filetype == "gff":
        start, stop = 3, 4
    for line in list_of_lists:
        if line[start] > line[stop]:
            line[stop], line[start] = line[start], line[stop]
            cnt += 1
    io.write_tsv(list_of_lists, out_filename)
    print("corrected ", str(cnt), "lines")
    return list_of_lists


def main():
    """
    Inputs: input file, output file, conversion function, other arguments
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_filename", help="input file to work with", required=True)
    parser.add_argument("-o", "--out", default="corrected.gff", help="output gff file")

    args = parser.parse_args()

    input_list_of_lists = io.read_tsv(args.input_filename)
    filetype = args.input_filename[-3:]

    correct_coord(input_list_of_lists, filetype, args.out)


if __name__ == "__main__":
    main()
