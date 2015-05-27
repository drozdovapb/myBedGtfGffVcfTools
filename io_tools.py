#!/usr/bin/env python3


def read_tsv(filename):
    """
    All flavors of gff, gtf, vcf, and bed files
    are just tab separated tables.
    This function takes a filename
    and returns a list of lists of strings
    """
    comment = '#'
    with open(filename, 'r') as fh:
        list_of_lists = []
        for line in fh:
            if not line.rstrip().startswith(comment):  # skip comment lines
                list_of_lists.append(line.rstrip().split('\t'))
    return list_of_lists


def write_tsv(list_of_lists, filename):
    """
    Takes a list of lists (list_obj) and writes a file
    This function doesn't return anything
    """
    with open(filename, 'w') as out:
        for line in list_of_lists:
            out.write('\t'.join(line) + '\n')
