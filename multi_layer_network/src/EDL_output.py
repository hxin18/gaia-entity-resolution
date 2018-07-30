import re
import sys
import getopt
import json

from collections import defaultdict


### Given EDL within document references and the connected components, outputs the results for evaluation. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:c:n:o:",["ifile=","cfile=","name=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given EDL within document references and the connected components, outputs the results for evaluation, usage: python EDL_output.py -i <inputfile> -c <connectedcomponents> -n <runname> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-c", "--cfile"):
			connectedcomponents = arg
		elif opt in ("-n", "--name"):
			runname = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	assign_to_clusters(inputfile, connectedcomponents, outputfile, runname)

def assign_to_clusters(path_to_within_document_references, path_to_clusters, path_to_output, run_name):
	clusters = defaultdict(set)
	counter = 0

	with open(path_to_clusters) as clusters_file:
		for line in clusters_file:
			clusters['cluster' + str(counter).zfill(7)] = set(json.loads(line[0:-1]))
			counter += 1
	# print clusters['cluster' + str(1).zfill(7)]

	with open(path_to_within_document_references) as r, open(path_to_output, 'w') as o:
		for line in r:
			within_document_cluster_id = re.split('\t', line)[4]
			found = False
			for cluster in clusters:
				if within_document_cluster_id in clusters[cluster]:
					pieces = re.split('\t', line)
					pieces[0] = run_name
					pieces[4] = cluster
					pieces[7] = '1.0\n'
					o.write('\t'.join(pieces))
					found = True
					break
			if not found:
				# raise Exception
				print(within_document_cluster_id)

if __name__ == '__main__':
	main(sys.argv[1:])
