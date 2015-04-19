#!/usr/bin/env python3

import sys


def __main__():
    file1_name, file2_name, output_name = sys.argv[1:]

    out = open(output_name, 'w')

#reading data

    with open(file1_name, 'r') as fh1:
        file1 = [line.split('\t') for line in fh1]

    with open(file2_name, 'r') as fh2:
        file2 = [line.split('\t') for line in fh2]

    file1_for_compare = [' '.join(line[:5]) for line in file1]  # only invariable information about SNPs in one string

#The actual comparison

    index = 0

    for line2 in file2:
        elem = str(' '.join(line2[:5]))
        if elem not in file1_for_compare[index:]:
            out.write('\t'.join(line2))
        else:
            index += 1


if __name__ == "__main__":
    __main__()
