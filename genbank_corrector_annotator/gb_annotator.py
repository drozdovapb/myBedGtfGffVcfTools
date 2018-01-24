#import
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import SeqFeature as sf
from Bio.Alphabet import generic_dna
import json
import sys

def annotate(my_plasmid, annot_dict):

    for key in annot_dict.keys():
        name = str(annot_dict[key]['label'])
        if my_plasmid.seq.find(key) > -1:
            start = my_plasmid.seq.find(key)
            end = start + len(key)
            #create new feature, put it in place and...
            new_feature = sf.SeqFeature(sf.FeatureLocation(start, end, strand=annot_dict[key]['strand']),
                                        type=annot_dict[key]['type'])
            #now append all the other features
            new_feature.qualifiers = annot_dict[key]
            ####https://www.biostars.org/p/57549/
            print('found ' + name)
            my_plasmid.features.append(new_feature)
        else:
            print(name + ' not found, trying complementary')
            comp = Seq(key, generic_dna).reverse_complement()
            if my_plasmid.seq.find(comp) > -1:
                start = my_plasmid.seq.find(comp)
                end = start + len(comp)
                #create new feature, put it in place and...
                new_feature = sf.SeqFeature(sf.FeatureLocation(start, end, strand=-1*annot_dict[key]['strand']),
                                            type=annot_dict[key]['type'])
    #            #now append all the other features
                new_feature.qualifiers = annot_dict[key]
    #           ####https://www.biostars.org/p/57549/
                print('found ' + name + ' in reverse complementary')
                my_plasmid.features.append(new_feature)
            else:
                print(name + ' not found')
    return my_plasmid



def main():
    if len(sys.argv) < 4:
        print('Please provide the following in this order: '
              'input genbank file, file with annotations, file to write output \n'
              'Example usage: python3 ./gb_annotator.py naked_map.gb feature_table.txt map_upd.gb')
        sys.exit(2)

    #read
    input_file, annot_dict_name = sys.argv[1:3]
    output = sys.argv[3]

    with open(annot_dict_name, 'r') as fh:
        annot_dict = json.load(fh)

    my_plasmid = SeqIO.read(input_file, 'genbank')

    my_plasmid_annot = annotate(my_plasmid, annot_dict)


    #Write output to file
    SeqIO.write(my_plasmid_annot, output, 'genbank')


if __name__ == "__main__":
    main()