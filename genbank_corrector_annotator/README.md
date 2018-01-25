## Plasmid correction

### Introduction

Full plasmid correction pipeline is a three-step process. However, you can use only the second step if you prefer to make annotations yourself. 

##### 1. Collect annotations that you will need later:

`python3 ./gb_annot_collector.py map1.gb map2.gb ... mapN.gb >collected_features.txt`

You can use both a new version of the backbone and 
If the system says 'cannot overwrite the existing file' but you do wanna overwrite the existing file, replace `>` with `>|`. 

##### 2. Correct plasmid sequence:

`python3 ./gb_annotator.py old_map.gb changes.txt <new_plasmid.gb>`

The last argument is optional. If it is not provided, the script creates a file with the same name as the input file in the `corrected` subfolder (creating the  subfolder if it does not exist). 

##### Annotate the new sequence

`python3 ./gb_annotator.py corrected_maps/new_map.gb collected_features.txt corrected_maps/new_map_annotate.gb`


#### Example data 

We will correct the pRS315-SUP45 map (Le Goff _et al._, 2002 // Genes to Cells). It was created using the NCBI-provided backbone and thus has some errors in its sequence.

We collect annotations:

`python3 ./gb_annot_collector.py pRS-true_maps/pRS315.gb pRS315-SUP45.gb >collected_features.txt`

Then correct the sequence:

`python3 ./gb_pRS_corrector.py pRS315-SUP45.gb pRS_diff_large.txt` 

Program output during correction:
	
    Initial length:  8962
	found the old version of LacZ_center2
	found the old version of pRS315_snapgene_LEU_side
	found the old version of pRS315_snapgene_LEU_side
	found the old version of LacZ_center1
	Final length:  8950
    Written the result to corrected_maps/pRS315-SUP45.gb

Please note that here we see that 2 "sides" were changed. This should happen with every plasmid. If it does not happen, please consider the possibility of checking manually (make an alignment and see what's wrong). In addition, consider using smaller portions (`pRS_diff_small`). Please note these are specific for each plasmid. 

Now, return the annotations to the plasmids:

`python3 ./gb_annotator.py corrected_maps/pRS315-SUP45.gb collected_features.txt corrected_maps/pRS315-SUP45.gb #we can also replace the existing map if we don't need it anymore`

Program output:

	found ['ARSH4']
	found ['T3 promoter']
	found ['AmpR promoter']
	['SK primer'] not found, trying complementary
	['SK primer'] not found
	found ['ori']
	found ['S45Ter']
	found ['F1_ORI']
	found ['CEN6']
	found ["NFS1-3'"]
	found ['LacZ_beginning']
	found ['KS primer']
	found ['lac operator']
	found ['SUP45']
	found ['T7 promoter']
	['LacZ-alpha'] not found, trying complementary
	['LacZ-alpha'] not found
	found ['M13 rev']
	found ['T3_P']
	found ['M13 fwd']
	found ['f1 ori']
	found ['LacZ_ending']
	found ['LacZ_center1']
	found ['tL(CAA)C / SUP53']
	found ['LEU2 promoter']
	found ['LEU2']
	['LEU2'] not found, trying complementary
	['LEU2'] not found
	['MCS'] not found, trying complementary
	['MCS'] not found
	found ['CAP binding site']
	found ["Ty2 LTR 3'-fragment"]
	found ['LEU2 / NFS1 terminator']
	found ['LacZ_center2']
	found ["f1 ori - 3'_ext"]
	found ['T7_P']
	found ['lac promoter']
	found ['AmpR']
	['AP(R)'] not found, trying complementary
	['AP(R)'] not found
	found ['PMB1']	
	found ['CEN/ARS']
	found ["SUP35_5'"]

This list may look overwhelming and complicated, but in fact it is not. If we look closer, we'll see that: (1) MCS [multiple cloning site] was not found, which is quite logical; (2) old AmpR (AP(R)) was not found, while the new sequence (AmpR) indeed was, and so on.

That's it!