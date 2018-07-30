import re
import sys
import json
import getopt
import gzip

from collections import defaultdict


### Given RPI ColdStart input, produces the JSON file that will be used by the rest of the pipeline. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given RPI ColdStart input, produces the JSON file that will be used by the rest of the pipeline, usage: python RPI_to_JSON.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	if '.gz' in inputfile:
		extract_canonical_mentions_as_cluster_heads_GZIP(inputfile, outputfile)
	else:
		extract_canonical_mentions_as_cluster_heads(inputfile, outputfile)

def extract_canonical_mentions_as_cluster_heads(path_to_KB_file, path_to_output, print_counter=False):
	cluster_heads = defaultdict(list)
	type_look_up_table = {}
	link_look_up_table = defaultdict(lambda: '')

	count = 0
	with open(path_to_KB_file) as KB:
		for line in KB:
			if print_counter:
				count += 1
				if count % 100000 == 0:
					print 'processing line ',str(count)
			fields = re.split('\t', line)
			if len(fields) < 2: continue
			if fields[1] == 'type':
				type_look_up_table[fields[0]] = fields[2][:-1]
			if fields[1] == 'link':
				link_look_up_table[fields[0]] = fields[2][:-1]

	count = 0
	with open(path_to_KB_file) as KB:
		for line in KB:
			if print_counter:
				count += 1
				if count % 100000 == 0:
					print 'processing line ',str(count)
			fields = re.split('\t', line)
			if len(fields) < 2: continue
			if fields[1] == 'canonical_mention':
				if fields[0][1:7] != 'Entity': continue

				cluster_heads[fields[0][1:] + ':' + re.split(':', fields[3])[0]].append(fields[2].lower())
				cluster_heads[fields[0][1:] + ':' + re.split(':', fields[3])[0]].append(type_look_up_table[fields[0]])
				cluster_heads[fields[0][1:] + ':' + re.split(':', fields[3])[0]].append(link_look_up_table[fields[0]])

	print(len(cluster_heads))

	with open(path_to_output, 'w') as output:
		json.dump(cluster_heads, output)


def extract_canonical_mentions_as_cluster_heads_GZIP(path_to_KB_file, path_to_output, print_counter=True):
	cluster_heads = defaultdict(list)
	type_look_up_table = {}
	link_look_up_table = defaultdict(lambda: '')
	count = 0

	with gzip.open(path_to_KB_file, 'r') as KB:
		for line in KB:
			if print_counter:
				count += 1
				if count % 100000 == 0:
					print 'processing line ',str(count)
			fields = re.split('\t', line)
			if len(fields) < 2: continue
			if fields[1] == 'type':
				type_look_up_table[fields[0]] = fields[2][:-1]
			if fields[1] == 'link':
				link_look_up_table[fields[0]] = fields[2][:-1]

	count = 0
	with gzip.open(path_to_KB_file) as KB:
		for line in KB:
			if print_counter:
				count += 1
				if count % 100000 == 0:
					print 'processing line ',str(count)
			fields = re.split('\t', line)
			if len(fields) < 2: continue
			if fields[1] == 'canonical_mention':
				if fields[0][1:7] != 'Entity': continue

				cluster_heads[fields[0][1:] + ':' + re.split(':', fields[3])[0]].append(fields[2].lower())
				cluster_heads[fields[0][1:] + ':' + re.split(':', fields[3])[0]].append(type_look_up_table[fields[0]])
				cluster_heads[fields[0][1:] + ':' + re.split(':', fields[3])[0]].append(link_look_up_table[fields[0]])

	print(len(cluster_heads)) # each cluster head contains three elements: canonical mention, type, EDL link

	with open(path_to_output, 'w') as output:
		json.dump(cluster_heads, output)

if __name__ == '__main__':
	main(sys.argv[1:])
