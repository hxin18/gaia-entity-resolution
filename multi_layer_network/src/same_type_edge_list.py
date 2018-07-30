import re
import sys
import json
import getopt
import networkx as nx

from collections import defaultdict


### Given the canonical mentions JSON file, a threshold, and edge weight option, produces the edge list corresponding to that. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:t:w:o:",["ifile=","threshold=","weight=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given the canonical mentions JSON file, produce the edge list such that all entities of the same type are clumped into the same cluster, usage: python same_type_edge_list.py -i <inputjsonfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	get_same_type_edge_list(inputfile, outputfile)

def get_same_type_edge_list(path_to_cluster_heads, path_to_output):
	cluster_heads = json.load(open(path_to_cluster_heads))

	IDs = list(cluster_heads.keys())

	G = nx.Graph()
	G.add_nodes_from(IDs)

	for i, id1 in enumerate(IDs):
		for j in range(i + 1, len(IDs)):
			id2 = IDs[j]
			if cluster_heads[id1][1] == cluster_heads[id2][1]:
					G.add_edge(id1, id2)

	with open(path_to_output, 'w') as output:
		output.write(str(G.nodes())  + '\n')
		for e in G.edges(data=True):
			output.write(str(e) + '\n')

# def get_string_jaccard_score(s1, s2, n_gram):
# 	set1 = set()
# 	set2 = set()
#
# 	for i in range(len(s1) - n_gram + 1):
# 		set1.add(s1[i:i + n_gram])
# 	for i in range(len(s2) - n_gram + 1):
# 		set2.add(s2[i:i + n_gram])
#
# 	return len(set1 & set2) / len(set1 | set2)

if __name__ == '__main__':
	main(sys.argv[1:])
