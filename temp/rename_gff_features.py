#!/usr/bin/env python3

import sys
import base_functions as bf
#import itertools

def main():
    gff_to_rename, gff_with_perfect_names, output_gff = sys.argv[1:]
    perfect_names = bf._read_tsv(gff_with_perfect_names)
    to_rename = bf._read_tsv(gff_to_rename)
    new_genes = []

    position = 0
    with open(output_gff, 'w') as out:
        for line_to_rename in to_rename:
            found = False
            for perfect_line in perfect_names:
                if line_to_rename[0] == perfect_line[0] \
                        and line_to_rename[3] == perfect_line[3] \
                        and line_to_rename[4] == perfect_line[4]:
                    #line_to_rename[:9].append(perfect_names[9])
                    #print("found!")
                    out.write('\t'.join(line_to_rename[:8]) + '\t' + perfect_line[8] + '\n')
                    found = True
            if not found:
                out.write('\t'.join(line_to_rename[:8]) + '\t' + 'new' + '\n')
                if line_to_rename[2] == 'gene':
                    new_genes.append(line_to_rename)

    for line in new_genes:
        print('\t'.join(line)+'\n')

if __name__ == "__main__":
    main()


#Test section
