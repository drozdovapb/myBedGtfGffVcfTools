#!/usr/bin/env python

import sys

assert sys.version_info[:2] >= (2, 4)

def __main__():
    input_name = sys.argv[1]
    output_name = sys.argv[2]


    out = open(output_name, 'w')

    features = list()
    with open(input_name, 'r') as fh1:
        for line in fh1:
            features.append(line.split('\t'))

    contigs = dict()
    strange_contigs = set()

#    for line in features:
#        if line[0] not in contigs:
#            contigs[line[0]] = line[3][1:3]
#            continue
#        elif line[0] in contigs:
#            if contigs[line[0]] == line[3][1:3]:
#                continue
#            else:
#                strange_contigs.add(line[0])


    for line in features:
        if line[0] not in contigs:
            contigs[line[0]] = line[3][1]
            continue
        elif line[0] in contigs:
            if contigs[line[0]] == line[3][1]:
                continue
            else:
                strange_contigs.add(line[0])

#    out.write('These contigs seem strange')
    out.write('\n'.join(strange_contigs))

#    out.write('Which genes do these contigs? have')


#    with open(input_name, 'r') as fh1:
#         for contig in strange_contigs:
#             out = [line.split('\t') for line in fh1 if contig in line]

#    out.write(out)



if __name__ == "__main__": __main__()