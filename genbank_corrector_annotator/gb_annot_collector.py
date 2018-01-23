#import packages
import json
import sys
import argparse
from Bio import SeqIO


def collect_annotations(file, annot_dict):
    """
    This script compiles a dictionary of all features in input genbank files and outputs them to stdout.
    Keys as sequences while values are all feature qualifiers
    (I thought it would be better to use all but this behaviour can be easily changed to just names).
    """
    #Process each plasmid
    #read a .gb file with the plasmid
    my_plasmid = SeqIO.read(file, 'genbank')

    #process each feature
    for feature in my_plasmid.features:
        ##print(feat)
        #nofuzzy is great!
        start = feature.location.nofuzzy_start
        end = feature.location.nofuzzy_end
        strand = feature.location.strand
        #now we need feature type
        type = feature.type
        #and all the other qualifiers
        qualif = feature.qualifiers  # it turns out to form a dictionary
        qualif['type'] = type
        qualif['strand'] = strand
        #and also location
        sequence = str(my_plasmid.seq[start:end])
        #Now collect a dictionary of dictionaries
        annot_dict[sequence] = qualif

    return annot_dict



def main():
    if len(sys.argv) < 2:
        print('Please provide some .gb files \n')

    output = sys.stdout
    files = sys.argv[1:]

    #create an empty annotation dictionary
    annot_dict = dict()

    for file in files:
        collect_annotations(file, annot_dict)

    #Write it to file
    json.dump(annot_dict, output)


if __name__ == "__main__":
    main()