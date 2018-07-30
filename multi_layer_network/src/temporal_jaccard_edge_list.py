import re
import sys
import json
import getopt
import networkx as nx

from datetime import datetime
from collections import defaultdict


### Given the canonical mentions JSON file, produces the edge list corresponding to that, taking temporal information into account. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given the canonical mentions JSON file, produces the edge list corresponding to that, taking temporal information into account, usage: python temporal_jaccard_edge_list.py -i <inputjsonfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	get_temporal_jaccard_edge_list(inputfile, outputfile)

def get_temporal_jaccard_edge_list(path_to_cluster_heads, path_to_output):
	cluster_heads = json.load(open(path_to_cluster_heads))

	IDs = list(cluster_heads.keys())

	G = nx.Graph()
	G.add_nodes_from(IDs)

	for i, id1 in enumerate(IDs):
		for j in range(i + 1, len(IDs)):
			id2 = IDs[j]
			if cluster_heads[id1][1] == cluster_heads[id2][1] and get_string_jaccard_score(cluster_heads[id1][0], cluster_heads[id2][0], 3) > 0.8:
				G.add_edge(id1, id2)
			elif cluster_heads[id1][1] == cluster_heads[id2][1]:
				if len(re.split('_', re.split(':', id1)[1])) == 5:
					id1_temporal_info = re.split('_', re.split(':', id1)[1])[3]
				# NYT Exception
				elif re.split(':', id1)[1][0:3] == 'NYT':
					id1_temporal_info = re.split('_', re.split(':', id1)[1])[2][0:8]
				if len(re.split('_', re.split(':', id2)[1])) == 5:
					id2_temporal_info = re.split('_', re.split(':', id2)[1])[3]
				# NYT Exception
				elif re.split(':', id2)[1][0:3] == 'NYT':
					id2_temporal_info = re.split('_', re.split(':', id2)[1])[2][0:8]
				id1_datetime = datetime.strptime(id1_temporal_info, '%Y%m%d')
				id2_datetime = datetime.strptime(id2_temporal_info, '%Y%m%d')

				difference = abs((id1_datetime - id2_datetime).days)

				if difference <= 3:
					if get_string_jaccard_score(cluster_heads[id1][0], cluster_heads[id2][0], 3) > 0.4:
						G.add_edge(id1, id2)
				elif difference <= 6:
					if get_string_jaccard_score(cluster_heads[id1][0], cluster_heads[id2][0], 3) > 0.6:
						G.add_edge(id1, id2)

	with open(path_to_output, 'w') as output:
		output.write(str(G.nodes())  + '\n')
		for e in G.edges:
			output.write(str(e) + '\n')

def get_string_jaccard_score(s1, s2, n_gram):
	set1 = set()
	set2 = set()

	for i in range(len(s1) - n_gram + 1):
		set1.add(s1[i:i + n_gram])
	for i in range(len(s2) - n_gram + 1):
		set2.add(s2[i:i + n_gram])

	return len(set1 & set2) / len(set1 | set2)

if __name__ == '__main__':
	main(sys.argv[1:])
