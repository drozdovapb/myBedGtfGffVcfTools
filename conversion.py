#!/usr/bin/env python3

import re


def read_tsv(filename):
    """
    Basically, all flavors of gff and gtf as well as vcf and bed files
    are just tab separated tables.
    This function takes a filename
    and returns a list of lists of strings
    """
    with open(filename, 'r') as fh:
        list_of_lists = []
        for line in fh:
            if not line.startswith('#'):  # skip comment lines
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
            # conversion to string used to avoid problems with integer coordinates


def id_gff2_to_gff3(attributes):
    # change and save gene_id
    attributes = re.sub(r'gene_id \"(\w*).*?"', 'ID=\g<1>', attributes)
    # change and save gene_name
    attributes = re.sub(r'gene_name \"(\w*).*?"', 'Name=\g<1>', attributes)
    # get rid of other details
    attributes = re.sub(r'gene_.*? \"(\w*).*?\";', '', attributes)
    return attributes


def gtf2gff3(gtf2_filename, gff3_filename, cds_only=True):
    """
    This function takes a gtf2 file (gtf2_filename),
    writes a gff3 file to gff3_fileliname
    and also returns a list of lists
    Optimized for feeding ProteinOrtho
    CDS only here is the default option, and it can be changed
    """
    gtf2 = read_tsv(gtf2_filename)
    gff3 = []
    with open(gff3_filename, 'w') as out:
        for line in gtf2:
            print(line[8])  # line[8] doesn't work for some strange reason but line[-1] does
            print(line[2])  # line[2:3] works but line[2] does not
            if cds_only:
                if line[2:3] == ['CDS']:
                    line[-1] = id_gff2_to_gff3(line[-1])
                    gff3.append(line)
            else:
                line[-1] = id_gff2_to_gff3(line[-1])
                gff3.append(line)
    write_tsv(gff3, gff3_filename)
    return gff3


def gff32gtf(gff3):
    """
    :param gff3:
    :return:
    """
    pass


def gff2bed(gff3_filename, bed_filename, fromfile=True):
    """
    All ***2bed functions are utterly useful for working with the UCSC genome browser
    This function takes a gtf/gff-like object or reads a file,
     writes a bed file and also returns a bed-like object
    This version supports short bed files only
    Future versions will support long bed files (12 fields)
    """
    gff3 = read_tsv(gff3_filename) if fromfile else gff3_filename
    bed = []
    for line in gff3:
        #bed used 0-based coords while gff uses 1-based coords
        chrom = line[0]
        start, stop = str(int(line[3])-1), line[4]
        bed.append([chrom, start, stop])
    write_tsv(bed, bed_filename)
    return bed


def bed2gff3(bed_filename, gff_filename, source='bed2gff'):
    """
    The idea is taken from galaxy (usegalaxy.org) but was sufficiently renewed
    This function takes a bed file,
    writes a gff3 file and also returns a gff3-like object
    Source may be explicitly specified by the user (eg the program used to obtain evidence)
    """
    bed = read_tsv(bed_filename)
    gff = []
    long_bed = len(bed[0]) == 12
    for line in bed:
        chrom = line[0]
        start = str(int(line[1]) + 1)
        end = line[2]
        # if there are only 3 fields (short bed) we do not have enough information
        score, strand, attributes = '0', '.', ''
        #bed formatted files do not store source, phase and type information. Alas
        feature_type = "gene"
        phase = '.'
        if long_bed:
            genename, score, strand = line[3:6]
            attributes = 'ID=' + genename
        gff.append([chrom, source, feature_type, start, end, score, strand, phase, attributes])
        # Some code to deal with introns will be here
    write_tsv(gff, gff_filename)
    return gff



#if __name__ == "__main__": main()  # to be applied


#Test section
#Some tests that shouldn't be here
#Everything below this line is to be replaced with proper tests

#path_to_test_files = "/media/drozdovapb/big/Studies/bioinformaticsinstitute/bio-py-14/myBedGtfGffVcfTools/test/"

#gff2bed(path_to_test_files + "test_augustus_gff3.gff",
#        "/media/drozdovapb/big/Studies/bioinformaticsinstitute/bio-py-14/test_out_bed")

#a = read_tsv("/media/drozdovapb/big/Studies/bioinformaticsinstitute/bio-py-14/myBedGtfGffVcfTools/test/test_augustus_gff3.gff")
#print(a[2:4])

#b = bed2gff3(path_to_test_files + "test_liftover.bed",
#        "/media/drozdovapb/big/Studies/bioinformaticsinstitute/bio-py-14/test_out_gff3",
#        "liftover")

#gtf2gff3('/media/drozdovapb/big/Peterhof_strains_seq/Annotation/Repeats/15V_contigs.fasta.out.gff',
#         '/media/drozdovapb/big/Peterhof_strains_seq/Annotation/Repeats/15V_repeatmasker_gff3.gff',
#         cds_only=False)