#!/usr/bin/env python3

import sys
from itertools import islice
from io_tools import read_tsv, write_tsv


def compare(reference, mutant):
    position = 0
    new_lines = []
    for mut_line in mutant:
        found = False
        for ref_line in islice(reference, position, None):
            if mut_line[:5] == ref_line[:5]:
                found = True
                position += 1
                break
        if not found:
            new_lines.append(mut_line)
    return new_lines


def main():

    if len(sys.argv) >= 3:
        reference_filename, mutant_filename = sys.argv[1:3]
        output_filename = sys.stdout
        if len(sys.argv) == 4:
            output_filename = sys.argv[3]
    else:
        print('Usage:' + '\n' +
              'compare_vcf.py <reference_filename> <mutant_filename> <output_filename>')
        sys.exit(2)

    reference = read_tsv(reference_filename)
    mutant = read_tsv(mutant_filename)

    result = compare(reference, mutant)

    write_tsv(result, output_filename)

if __name__ == "__main__":
    main()