#!/usr/bin/env python3

import sys
import io_tools as io


#it returns new genes. do i need this?

def main():
    gff_to_rename, gff_with_perfect_names, output_gff = sys.argv[1:]
    perfect_names = io.read_tsv(gff_with_perfect_names)
    strain = '15V' # add parser!
    to_rename = io.read_tsv(gff_to_rename)
    new_genes = []

    new_gene_count = 0
    with open(output_gff, 'w') as out:
        for line_to_rename in to_rename:
            found = False
            for perfect_line in perfect_names:
                # the same contig, the same start or end
                if line_to_rename[0] == perfect_line[0] \
                        and (line_to_rename[3] == perfect_line[3]
                             or line_to_rename[4] == perfect_line[4]):
                    #change the next line to something more flexible
                    out.write('\t'.join(line_to_rename[:8]) + '\t' + perfect_line[8] + '_15V-P4' + '\n')
                    found = True
            if not found:
                out.write('\t'.join(line_to_rename[:8]) + '\t' + 'ID=new_gene_' + str(new_gene_count) + '\n')
                if line_to_rename[2] == 'gene' and 'trna' not in line_to_rename[8]: #we don't need 'new' tRNA genes
                    print('\t'.join(line_to_rename[:8]) + '\t' + 'ID=new_gene_' + str(new_gene_count))
                    new_genes.append(line_to_rename)
                    new_gene_count += 1


if __name__ == "__main__":
    main()

