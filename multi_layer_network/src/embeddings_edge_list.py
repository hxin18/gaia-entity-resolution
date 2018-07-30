import re
import sys
import json
import getopt
import numpy as np
import networkx as nx

from collections import defaultdict


### Given the canonical mentions JSON file, the embeddings file, the embedding size, a threshold, and edge weight option, produces the edge list corresponding to that. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:e:s:t:w:o:",["ifile=","efile=","size=","threshold=","weight=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given the canonical mentions JSON file, the embeddings file, the embedding size, a threshold, and edge weight option, produces the edge list corresponding to that, usage: python embeddings_edge_list.py -i <inputjsonfile> -e <embeddingsfile> -s <embeddingsize> -t <threshold> -w <0/1> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-e", "--efile"):
			embeddingsfile = arg
		elif opt in ("-s", "--size"):
			size = int(arg)
		elif opt in ("-t", "--threshold"):
			threshold = float(arg)
		elif opt in ("-w", "--weight"):
			weight = int(arg)
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	get_embeddings_edge_list(inputfile, embeddingsfile, size, threshold, weight, outputfile)

def get_embeddings_edge_list(path_to_cluster_heads, path_to_cluster_heads_vecs, embedding_size, cosine_threshold, weight_option, path_to_output):
	cluster_heads = json.load(open(path_to_cluster_heads))

	cluster_heads_vecs_mapping = {}

	vecs = np.zeros((len(cluster_heads), embedding_size))
	with open(path_to_cluster_heads_vecs) as vecs_file:
		for i, line in enumerate(vecs_file):
			cluster_head_id = line[:-1].split()[0]
			cluster_head_vec = np.array([float(x) for x in line[:-1].split()[1:]])
			cluster_heads_vecs_mapping[cluster_head_id] = i
			vecs[i] = cluster_head_vec / np.sqrt(cluster_head_vec.dot(cluster_head_vec))

	cosine_similarities = np.matmul(vecs, vecs.T)

	IDs = list(cluster_heads.keys())

	G = nx.Graph()
	G.add_nodes_from(IDs)

	for i, id1 in enumerate(IDs):
		for j in range(i + 1, len(IDs)):
			id2 = IDs[j]
			if cluster_heads[id1][1] == cluster_heads[id2][1] and cosine_similarities[cluster_heads_vecs_mapping[id1]][cluster_heads_vecs_mapping[id2]] > cosine_threshold:
				if weight_option == 1:
					G.add_edge(id1, id2, weight=cosine_similarities[cluster_heads_vecs_mapping[id1]][cluster_heads_vecs_mapping[id2]])
				else:
					G.add_edge(id1, id2)

	with open(path_to_output, 'w') as output:
		output.write(str(G.nodes()) + '\n')
		for e in G.edges(data=True):
			output.write(str(e) + '\n')

if __name__ == '__main__':
	main(sys.argv[1:])
