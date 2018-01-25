#import packages
import json
import sys
#import argparse #this particular script does not parse anything
from Bio import SeqIO


def collect_annotations(file, annot_dict):
    """
    This script compiles a dictionary of all features in input genbank files and outputs them to stdout.
    Keys as sequences while values are all feature qualifiers
    """
    #Load plasmid
    #read a .gb file with the plasmid
    my_plasmid = SeqIO.read(file, 'genbank')

    #process each feature
    for feature in my_plasmid.features:
        #get the start and end positions for the feature
        start = feature.location.nofuzzy_start
        end = feature.location.nofuzzy_end
        #todo write some code to deal with split features
        #get strand to correctly place directed features like ORF
        strand = feature.location.strand
        #get feature type
        type = feature.type
        #and all the other qualifiers
        qualif = feature.qualifiers  # it's a dictionary
        qualif['type'] = type
        qualif['strand'] = strand
        #and also location
        sequence = str(my_plasmid.seq[start:end])
        #Now collect a dictionary of dictionaries
        annot_dict[sequence] = qualif

    return annot_dict



def main():
    if len(sys.argv) < 2:  # if no file is provided
        print('Please provide some .gb files \n')

    output = sys.stdout
    files = sys.argv[1:]
    # This alternative should work better with piped ls input
    #files = [map.strip('\n') for map in sys.stdin.readlines()]

    #create an empty annotation dictionary
    annot_dict = dict()

    #And now process each file
    for file in files:
        collect_annotations(file, annot_dict)

    #Write it to file
    json.dump(annot_dict, output)


if __name__ == "__main__":
    main()