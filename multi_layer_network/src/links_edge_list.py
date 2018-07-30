import re
import sys
import json
import getopt
import networkx as nx

from collections import defaultdict


### Given the canonical mentions JSON file, produces the edge list corresponding to that. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given the canonical mentions JSON file, produces the edge list corresponding to that, usage: python links_edge_list.py -i <inputjsonfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	get_links_edge_list(inputfile, outputfile)

def get_links_edge_list(path_to_cluster_heads, path_to_output):
	cluster_heads = json.load(open(path_to_cluster_heads))

	IDs = list(cluster_heads.keys())

	G = nx.Graph()
	G.add_nodes_from(IDs)

	for i, id1 in enumerate(IDs):
		for j in range(i + 1, len(IDs)):
			id2 = IDs[j]
			if cluster_heads[id1][1] == cluster_heads[id2][1] and cluster_heads[id1][2] == cluster_heads[id2][2] and cluster_heads[id1][2]!= '':
				G.add_edge(id1, id2)

	with open(path_to_output, 'w') as output:
		output.write(str(G.nodes()) + '\n')
		for e in G.edges:
			output.write(str(e) + '\n')

# if __name__ == '__main__':
# 	main(sys.argv[1:])
#get_links_edge_list('/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling_cluster_heads.json',
#					'/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling_same_link.edgelist')
