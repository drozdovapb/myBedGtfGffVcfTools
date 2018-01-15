#import packages
from Bio import SeqIO
from Bio.Seq import Seq
import json
import string
from Bio.Alphabet import generic_dna
#from Bio import SeqFeature as sf
#import gb_annotator
import sys


def edit_sequence(my_plasmid, changes_dict):
    n_seqs_changed = 0
    mutable_seq = str(my_plasmid.seq)
    #print(len(mutable_seq))
    #collect all replaced nucleotides
    replaced = set()
    for feature in changes_dict.keys():
        #print(changes_dict[feature]['label'], mutable_seq.find(feature))
        position_found = mutable_seq.find(feature)
        if position_found > 0:
            n_seqs_changed += 1
            print('found the old version of ', changes_dict[feature]['label'])
            mutable_seq = mutable_seq.replace(feature, changes_dict[feature]['true'])
            position_end = position_found + len(feature)
            replaced_now = set(range(position_found, position_end + 1))
            replaced = replaced.union(replaced_now)  # for some reason it does not update itself
        else:
            comp_old = str(Seq(feature, generic_dna).reverse_complement())
            position_found = mutable_seq.find(comp_old)
            if position_found > 0:
                n_seqs_changed += 1
                print('found the old version of ', changes_dict[feature]['label'])
                comp_true = str(Seq(changes_dict[feature]['true'], generic_dna).reverse_complement())
                mutable_seq = mutable_seq.replace(comp_old, comp_true)
                position_end = position_found + len(feature)
                replaced_now = set(range(position_found, position_end + 1))
                replaced = replaced.union(replaced_now)  # for some reason it does not update itself
    if n_seqs_changed < 2:
        print('only ' + str(n_seqs_changed) + ' parts were changed. Please check manually')

    #remove plasmid features because they are now wrong
    my_plasmid.features = [] #make a copy, otherwise it will edit both lists!


    return my_plasmid

def main():
    if len(sys.argv) < 3:
        print('Please provide the following in this order: '
              'input genbank file, changes dictionary '
              'Example usage: python3 ./gb_annotator.py old_map.gb changes.txt')
        sys.exit(2)


    #read a .gb file with the plasmid
    my_plasmid_name = sys.argv[1]
    my_plasmid = SeqIO.read('' + my_plasmid_name, 'genbank')

    with open(sys.argv[2], 'r') as fh:
        changes_dict = json.load(fh)
#    #and add new ones
#    with open(sys.argv[3], 'r') as fh:
#        new = json.load(fh)

    my_plasmid = edit_sequence(my_plasmid, changes_dict)
#    my_plasmid = gb_annotator.annotate(my_plasmid, new)
    print(len(my_plasmid.seq))

    SeqIO.write(my_plasmid, 'new_maps/' + my_plasmid_name, 'genbank')

if __name__ == "__main__":
    main()
