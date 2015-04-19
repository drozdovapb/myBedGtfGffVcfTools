#!/usr/bin/env python3

import sys


def __main__():
    input_name, output_name = sys.argv[1:]

    out = open(output_name, 'w')

#importing the bed file

    with open(input_name, 'r') as fh1:
        features = [line.split('\t') for line in fh1]

    contigs = dict()
    strange_contigs = set()

    for line in features:
        if line[0] not in contigs:
#here we fill a dictionary of contig names (keys) and chromosomes that host the genes found (values)
            contigs[line[0]] = line[3][1]
            continue
        elif line[0] in contigs:
#here we check whether second (and further genes) found in the same contig
# elif is used instead of else for clarity (I'm not really sure about it)
            if contigs[line[0]] == line[3][1]:
                continue
            else:  # if the first letter (i.e. chromosome name) differs for different genes
                strange_contigs.add(line[0])

    #out.write('These contigs seem strange')
#writing output
    out.write('\n'.join(strange_contigs))


if __name__ == "__main__":
    __main__()