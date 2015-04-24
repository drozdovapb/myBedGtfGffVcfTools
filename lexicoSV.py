#!/usr/bin/env python3

import sys


def __main__():
    input_name, output_name = sys.argv[1:]

#importing the bed file
    with open(input_name, 'r') as fh1:
        features = [line.split('\t') for line in fh1]

    contigs = dict()
    strange_contigs = set()

    for line in features:
        contig_name = line[0]
        chr_letter = line[3][1]

        if contig_name not in contigs:
        #filling a dictionary of contig names (keys) and chromosomes that host the genes (values)
            contigs[contig_name] = chr_letter
            continue
        #if contig_name in contigs:
        #here we check whether second (and further genes) found in the same contig
        if contigs[contig_name] == chr_letter:
            continue
        # if the first letter (i.e. chromosome name) differs for different genes
        strange_contigs.add(contig_name)

#writing output
    with open(output_name, 'w') as out:
        out.write('\n'.join(strange_contigs))


if __name__ == "__main__":
    __main__()