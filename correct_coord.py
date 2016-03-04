#!/usr/bin/env python3

import argparse
import os
import io_tools as io
import sys

def correct_coord(list_of_lists, filetype, out_filename):
    """
    Flips the coordinates if the start coordinate is greater than stop.
    """
    cnt = 0
    if filetype == ".bed":
        start, stop = 1, 2
        shift = 1  # bed is ZERO-based
    elif filetype == ".gff":
        start, stop = 3, 4
        shift = 0  # gff is ONE-based
    for line in list_of_lists:
        if int(line[start]) > int(line[stop]):
            newstart = str(int(line[stop]) - shift)
            newstop = str(int(line[start]) + shift)
            line[start], line[stop] = newstart, newstop
            cnt += 1
    io.write_tsv(list_of_lists, out_filename)
    print("corrected ", str(cnt), "lines")


def main():
    """
    Inputs: input file, output file name
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_filename", help="input file to work with", required=True)
    parser.add_argument("-o", "--out", default="corrected.gff", help="output gff / bed file")

    args = parser.parse_args()

    input_list_of_lists = io.read_tsv(args.input_filename)
    filetype = os.path.splitext(args.input_filename)[1]
    if filetype not in [".bed", ".gff"]:
        print("Unknown file extension. Please make sure you have a .bed or .gff file")
        sys.exit("Unknown file type")

    correct_coord(input_list_of_lists, filetype, args.out)


if __name__ == "__main__":
    main()
