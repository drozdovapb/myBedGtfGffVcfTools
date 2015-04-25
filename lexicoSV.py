#!/usr/bin/env python3

import sys


def check_for_peculiarities(list_of_features):
    """
    This function takes a list of features (genes and coordinates)
    and checks whether each contig contains only adjacent genes.
    If it is not the case it reports the name of the contig.
    Such contigs may result from either chromosomal rearrangement
    or assembly / annotation errors.
    """

    contigs = dict()  # a distionary of contig names and chromosomes
    strange_contigs = set()  # stores names of contigs with non-adjacent genes
    for line in list_of_features:
        contig_name = line[0]
        chr_letter = line[3][1]

        if contig_name not in contigs:  # fill the dictionary
            contigs[contig_name] = chr_letter
            continue

        # check other genes in the same contig
        if contigs[contig_name] == chr_letter:  # the contig is ok
            continue

        strange_contigs.add(contig_name)

    return strange_contigs


def main():
    input_name, output_name = sys.argv[1:]

    with open(input_name, 'r') as fh1:
        features = [line.split('\t') for line in fh1]

    strange_contigs = check_for_peculiarities(features)

    with open(output_name, 'w') as out:
        out.write('\n'.join(strange_contigs))


if __name__ == "__main__":
    main()