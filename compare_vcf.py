#!/usr/bin/env python3

import sys
from itertools import islice
from io_tools import read_tsv, write_tsv


def main():
    reference_filename, mutant_filename, output_filename = sys.argv[1:]

#    to_stdout = False

    if len(sys.argv) == 4:
        reference_filename, mutant_filename, output_filename = sys.argv[1:]
#    elif len(sys.argv) == 3:
#        reference_filename, mutant_filename = sys.argv[1:]
#        to_stdout = True
    else:
        print('Usage:' + '\n' +
              'compare_vcf.py <reference_filename> <mutant_filename> <output_filename>')
        sys.exit(2)


    #reading data
    reference = read_tsv(reference_filename)
    mutant = read_tsv(mutant_filename)

    # unique information for each variant
    reference_variants = [' '.join(line[:5]) for line in reference]

    #The actual comparison
    position = 0
    with open(output_filename, 'w') as out:
        for line in mutant:
            variant = ' '.join(line[:5])  # unique information for this variant
            if variant not in islice(reference_variants, position, None):
                    out.write('\t'.join(line))
            else:
                position += 1


if __name__ == "__main__":
    main()
