#!/usr/bin/env python3

import sys
import io_tools as io


def main():
    gff_to_rename, table_for_rename, output_gff = sys.argv[1:]
    table = io.read_tsv(table_for_rename)
    strain = ''  # add parser!
    to_rename = io.read_tsv(gff_to_rename)
    new_genes = []

    new_gene_count = 0
    with open(output_gff, 'w') as out:
        for line_to_rename in to_rename:
            if line_to_rename[2] == 'mRNA':
                found = False
                for cluster in table:
                    #exchange the next two lines if necessary (depends on the order in the table)
                    #maker_name = cluster[3][:-27] #unique part of the name
                    #maker_name = cluster[3][:-7] #unique part of the name if using augustus
                    maker_name = cluster[3]  # [:7] is not truly unique because there might be '01' and '013'
                    #print(maker_name)
                    proper_name = cluster[4]
                    if maker_name in line_to_rename[8]:
                        out.write('\t'.join(line_to_rename[:8]) + '\t' + 'ID=' + proper_name + '\n')  # '_' + strain
                        #print('yeap')
                        found = True
    #                    continue
                if not found:
                    out.write('\t'.join(line_to_rename[:8]) + '\t' + 'ID=new_gene_' + str(new_gene_count) + '\n')
                    if line_to_rename[2] == 'mRNA' and 'trna' not in line_to_rename[8]:  # we don't need 'new' tRNA genes
                        print('\t'.join(line_to_rename[:8]) + '\t' + 'ID=new_gene_' + str(new_gene_count))
                        new_genes.append(line_to_rename)
                        new_gene_count += 1


if __name__ == "__main__":
    main()

