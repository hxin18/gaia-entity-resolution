import re
import sys
import getopt
import networkx as nx

from ast import literal_eval


### Given two edge lists, combines them by either union or intersection. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:e:m:o:",["ifile=","efile=","method=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given two edge lists, combines them by either union or intersection, usage: python combine_edge_lists.py -i <firstedgelist> -e <secondedgelist> -m <u/i> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			firstedgelist = arg
		elif opt in ("-e", "--efile"):
			secondedgelist = arg
		elif opt in ("-m", "--method"):
			method = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	G1 = nx.Graph()
	G2 = nx.Graph()

	with open(firstedgelist) as edges:
		G1.add_nodes_from(literal_eval(edges.readline()))
		for edge in edges:
			edge_nodes = literal_eval(edge)
			G1.add_edge(edge_nodes[0], edge_nodes[1])

	with open(secondedgelist) as edges:
		G2.add_nodes_from(literal_eval(edges.readline()))
		for edge in edges:
			edge_nodes = literal_eval(edge)
			G2.add_edge(edge_nodes[0], edge_nodes[1])

	G3 = nx.Graph()
	nodes = G1.nodes()
	G3.add_nodes_from(nodes)
	nodes = list(nodes)

	for i, node in enumerate(nodes):
		for other_node in nodes[i+1:]:
			if method == "u":
				if G1.has_edge(node, other_node) or G2.has_edge(node,other_node):
					G3.add_edge(node, other_node)
			elif method == "i":
				if G1.has_edge(node, other_node) and G2.has_edge(node,other_node):
					G3.add_edge(node, other_node)

	with open(outputfile, 'w') as output:
		output.write(str(G3.nodes()) + '\n')
		for e in G3.edges:
			output.write(str(e) + '\n')

if __name__ == '__main__':
	main(sys.argv[1:])
