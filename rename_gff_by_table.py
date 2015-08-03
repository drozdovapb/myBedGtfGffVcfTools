#!/usr/bin/env python3

import sys
import io_tools as io


def main():
    gff_to_rename, table_for_rename, output_gff = sys.argv[1:]
    table = io.read_tsv(table_for_rename)
    strain = '15V'  # add parser!
    to_rename = io.read_tsv(gff_to_rename)
    new_genes = []

    new_gene_count = 0
    with open(output_gff, 'w') as out:
        for line_to_rename in to_rename:
            found = False
            #print('fir', line_to_rename[8])
            for perfect_line in table:
                #print('sec', perfect_line[4][:-7])
                #if gene name in table
                if perfect_line[4][:-7] in line_to_rename[8]:
                    #change the next line to something more flexible
                    out.write('\t'.join(line_to_rename[:8]) + '\t' + perfect_line[3] + '_' + strain + '\n')
                    found = True
            if not found:
                out.write('\t'.join(line_to_rename[:8]) + '\t' + 'ID=new_gene_' + str(new_gene_count) + '\n')
                if line_to_rename[2] == 'gene' and 'trna' not in line_to_rename[8]:  # we don't need 'new' tRNA genes
                    print('\t'.join(line_to_rename[:8]) + '\t' + 'ID=new_gene_' + str(new_gene_count))
                    new_genes.append(line_to_rename)
                    new_gene_count += 1


if __name__ == "__main__":
    main()

