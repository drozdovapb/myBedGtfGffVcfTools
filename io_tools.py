#!/usr/bin/env python3

import sys


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


def _write_out(list_of_lists, output):
    for line in list_of_lists:
        output.write('\t'.join(line) + '\n')


def write_tsv(list_of_lists, filename=sys.stdout):
    """
    Takes a list of lists (list_obj) and writes a file (or to stdout)
    This function doesn't return anything
    """
    if filename is sys.stdout:
        _write_out(list_of_lists, sys.stdout)
    else:
        with open(filename, 'w') as out:
            _write_out(list_of_lists, out)