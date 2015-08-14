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
            for cluster in table:
                #exchange the next two lines if necessary (depends on the order in the table)
                maker_name = cluster[3][:-27] #unique part of the name
                proper_name = cluster[4]
                if maker_name in line_to_rename[8]:
                    #print('ldfj')
                    #print(maker_name)
                    #print(line_to_rename)
                    #change the next line to something more flexible
                    out.write('\t'.join(line_to_rename[:8]) + '\t' + proper_name + '_' + strain + '\n')
                    found = True
            if not found:
                out.write('\t'.join(line_to_rename[:8]) + '\t' + 'ID=new_gene_' + str(new_gene_count) + '\n')
                if line_to_rename[2] == 'gene' and 'trna' not in line_to_rename[8]:  # we don't need 'new' tRNA genes
                    print('\t'.join(line_to_rename[:8]) + '\t' + 'ID=new_gene_' + str(new_gene_count))
                    new_genes.append(line_to_rename)
                    new_gene_count += 1


if __name__ == "__main__":
    main()

