#!/usr/bin/env python3

import sys


def read_vcf(filename):
    with open(filename, 'r') as fh:
        return [line.split('\t') for line in fh]


def __main__():
    file1_name, file2_name, output_name = sys.argv[1:]

#reading data
    file1 = read_vcf(file1_name)
    file2 = read_vcf(file2_name)

    file1_for_compare = [' '.join(line[:5]) for line in file1]
    # only invariable information about SNPs in one string

#The actual comparison
    index = 0
    for line2 in file2:
        elem = str(' '.join(line2[:5]))
        if elem not in file1_for_compare[index:]:
            with open(output_name, 'w') as out:
                out.write('\t'.join(line2))
        else:
            index += 1


if __name__ == "__main__":
    __main__()
