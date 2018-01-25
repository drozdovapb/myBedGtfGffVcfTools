#import packages
from Bio import SeqIO
from Bio.Seq import Seq
import json
from Bio.Alphabet import generic_dna
import sys
import os


def edit_sequence(my_plasmid, changes_dict):
    #start counting found sequences to report if something looks not right
    n_seqs_changed = 0
    #make plasmid sequence mutable (to replace parts)
    mutable_seq = str(my_plasmid.seq)
    #loop through features
    for feature in changes_dict.keys():
        # try to find features (if not found it's -1)
        position_found = mutable_seq.find(feature)
        if position_found > -1:
            n_seqs_changed += 1  # we found 1 feature more, record it
            #and let the user know what we've found:
            print('found the old version of', changes_dict[feature]['label'])
            #replace with the correct sequence
            mutable_seq = mutable_seq.replace(feature, changes_dict[feature]["true"])
        #if not found try reverse complement
        else:
            comp_old = str(Seq(feature, generic_dna).reverse_complement())
            position_found = mutable_seq.find(comp_old)
            #if found in reverse complement:
            if position_found > -1:
                n_seqs_changed += 1  # again, let the user know we've found something
                print('found the old version of', changes_dict[feature]['label'])
                #prepare reverse complement of the true sequence
                comp_true = str(Seq(changes_dict[feature]['true'], generic_dna).reverse_complement())
                #
                mutable_seq = mutable_seq.replace(comp_old, comp_true)
    #if nothing or only one region was changed:
    if n_seqs_changed < 2:
        #let the user know s
        print('only ' + str(n_seqs_changed) + ' parts were changed. Please check manually')

    #now replace plasmid sequence with the one we've just corrected
    my_plasmid.seq = Seq(mutable_seq, generic_dna)
    #remove plasmid features because they are now mostly wrong
    my_plasmid.features = []

    return my_plasmid


def main():
    if len(sys.argv) < 3:  # if not enough filenames provided
        print('Please provide the following in this order: '
              'input genbank file, changes dictionary, new file name (optional) '
              'Example usage: python3 ./gb_annotator.py old_map.gb changes.txt <new_plasmid.gb>')
        sys.exit(2)


    #read a .gb file with the plasmid
    my_plasmid_name = sys.argv[1]
    my_plasmid = SeqIO.read(my_plasmid_name, 'genbank')
    #print initial plasmid length for information
    print('Initial length: ', len(my_plasmid.seq))

    #load changes dictionary
    with open(sys.argv[2], 'r') as fh:
        changes_dict = json.load(fh)

    #edit sequence
    my_plasmid = edit_sequence(my_plasmid, changes_dict)

    #and print final length to compare
    print('Final length: ', len(my_plasmid.seq))

    #create the output subdirectory if it does not exist
    if not os.path.exists('corrected_maps/'):
        os.makedirs('corrected_maps/')

    #construct output filename if it was provided by the user
    if len(sys.argv) == 4:
        new_filename = 'corrected_maps/' + sys.argv[3]
    #construct output filename if it was not provided explicitly
    else:
        my_plasmid_filename = os.path.basename(my_plasmid_name)
        new_filename = 'corrected_maps/' + my_plasmid_filename

    #write the final plasmid (it is not annotated)
    SeqIO.write(my_plasmid, new_filename, 'genbank')
    #and tell the user where we saved it
    print('Written the result to corrected_maps/' + my_plasmid_filename)

if __name__ == "__main__":
    main()
