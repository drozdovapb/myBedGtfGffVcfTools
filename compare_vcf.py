#!/usr/bin/env python3

import sys
import itertools


def read_vcf(filename):
    with open(filename, 'r') as fh:
        return [line.split('\t') for line in fh]


def main():
    reference_filename, mutant_filename, output_filename = sys.argv[1:]

    #reading data
    reference = read_vcf(reference_filename)
    mutant = read_vcf(mutant_filename)

    # unique information for each variant
    reference_variants = [' '.join(line[:5]) for line in reference]

    #The actual comparison
    position = 0
    with open(output_filename, 'w') as out:
        for line in mutant:
            variant = ' '.join(line[:5])  # unique information for this variant
            if variant not in itertools.islice(reference_variants, position, None):
                    out.write('\t'.join(line))
            else:
                position += 1


if __name__ == "__main__":
    main()