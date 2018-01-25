#import
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import SeqFeature as sf
from Bio.Alphabet import generic_dna
import json
import sys

def annotate(my_plasmid, annot_dict):
    """ This function takes a plasmid map (.gb) and a dictionary of features
    (such as created by gb_annot_collector)
    and adds these features to the plasmid if they are found
    """

    #loop through sequences in the dictionary
    for key in annot_dict.keys():
        #create a variable for the feature label for convenience (we'll use it couple more times)
        name = str(annot_dict[key]['label'])
        #try to find this sequence
        if my_plasmid.seq.find(key) > -1:
            #get start and end coordinates
            start = my_plasmid.seq.find(key)
            end = start + len(key)
            #create new feature, put it in place and...
            new_feature = sf.SeqFeature(sf.FeatureLocation(start, end, strand=annot_dict[key]['strand']),
                                        type=annot_dict[key]['type'])
            #now append all the other features
            new_feature.qualifiers = annot_dict[key]
            #add it to the plasmid features
            my_plasmid.features.append(new_feature)
            #and let the user know we've found something
            print('found ' + name)
        else:  # if the feature is not found try reverse complement
            #let the user know about it
            print(name + ' not found, trying complementary')
            #make reverse complement
            comp = Seq(key, generic_dna).reverse_complement()
            #try to find reverse complement
            if my_plasmid.seq.find(comp) > -1:
                #get start and end coordinates
                start = my_plasmid.seq.find(comp)
                end = start + len(comp)
                #create new feature, put it in place and...
                new_feature = sf.SeqFeature(sf.FeatureLocation(start, end, strand=-1*annot_dict[key]['strand']),
                                            type=annot_dict[key]['type'])
                #now append all the other features
                new_feature.qualifiers = annot_dict[key]
                #add it to the plasmid features
                my_plasmid.features.append(new_feature)
                #let the user know we've found something
                print('found ' + name + ' in reverse complementary')
            else:  # if not found in either strand
                print(name + ' not found')  # let the user know about it
    return my_plasmid


def main():
    if len(sys.argv) < 4:  # if not enough arguments
        print('Please provide the following in this order: '
              'input genbank file, file with annotations, file to write output \n'
              'Example usage: python3 ./gb_annotator.py naked_map.gb feature_table.txt map_upd.gb')
        sys.exit(2)

    #read input file names
    input_file, annot_dict_name = sys.argv[1:3]
    output = sys.argv[3]

    #read the plasmid
    my_plasmid = SeqIO.read(input_file, 'genbank')

    #load annotation dictionary
    with open(annot_dict_name, 'r') as fh:
        annot_dict = json.load(fh)

    #annotate the plasmid
    my_plasmid_annot = annotate(my_plasmid, annot_dict)

    #Write output to file
    SeqIO.write(my_plasmid_annot, output, 'genbank')


if __name__ == "__main__":
    main()