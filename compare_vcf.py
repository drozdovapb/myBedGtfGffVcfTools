#!/usr/bin/env python

import sys

def __main__():
    file1_name = sys.argv[1]
    file2_name = sys.argv[2]
    output_name = sys.argv[3]

    out = open(output_name, 'w')

#reading files

    file1 = list()
    with open(file1_name, 'r') as fh1:
        for line in fh1:
            file1.append(line.split('\t'))
            #out.write(line)

    file2 = list()
    with open(file2_name, 'r') as fh2:
        for line in fh2:
            file2.append(line.split('\t'))
            #out.write(line)

    file1_for_compare = list()  # this list includes only the invariable information about a SNP
    for line in file1:
        file1_for_compare.append(str(' '.join(line[:5])))

#The actual comparison

    index = 0

    for line2 in file2:
        elem = str(' '.join(line2[:5]))
        if elem not in file1_for_compare[index:]:
            out.write('\t'.join(line2))
        else:
            index += 1



if __name__ == "__main__": __main__()
