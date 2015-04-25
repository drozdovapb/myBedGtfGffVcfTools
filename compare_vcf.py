#!/usr/bin/env python3

import sys


def read_vcf(filename):
    with open(filename, 'r') as fh:
        return [line.split('\t') for line in fh]


def main():
    reference_name, mutant_name, output_name = sys.argv[1:]

    #reading data
    reference = read_vcf(reference_name)
    mutant = read_vcf(mutant_name)

    # unique information for each variant
    reference_variants = [' '.join(line[:5]) for line in reference]

    #The actual comparison
    index = 0
    with open(output_name, 'w') as out:
        for line in mutant:
            variant = ' '.join(line[:5])  # unique information for this variant
            if variant not in reference_variants[index:]:
                    out.write('\t'.join(line))
            else:
                index += 1


if __name__ == "__main__":
    main()