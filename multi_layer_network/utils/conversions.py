import re

path = '/Users/mayankkejriwal/git-projects/gaia-entity-resolution/multi_layer_network/'

def convert_edl_to_full_recall(in_file=path+'output_dir/out.edl', out_file=path+'output_dir1/out.edl'):
    out = open(out_file, 'w')
    with open(in_file, 'r') as f:
        for line in f:

            obj = re.split('\t', line[0:-1])
            # if len(obj) !=
            obj[4] = 'cluster0000001'
            out.write('\t'.join(obj)+'\n')
    out.close()

convert_edl_to_full_recall()
