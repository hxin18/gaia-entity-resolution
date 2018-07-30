import re
import sys
import getopt
import networkx as nx
import json

from ast import literal_eval


### Given an edge list, outputs the connected components. ###

# edgelist = '/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling_same_link.edgelist'
# outputfile = '/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling_same_link_clusters.jl'

def main(argv):
    opts, _ = getopt.getopt(argv, "he:o:", ["efile=", "ofile="])

    for opt, arg in opts:
        if opt == '-h':
            print(
                'Given an edge list, outputs the connected components, usage: python connected_components.py -e <edgelist> -o <outputfile>')
            sys.exit()
        elif opt in ("-e", "--efile"):
            edgelist = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    G = nx.Graph()
    # edgelist = '/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling_same_link.edgelist'
    # outputfile = '/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling_same_link_clusters.jl'
    path_to_cluster_heads = "/Users/xinhuang/Downloads/gaia-entity-resolution/multi_layer_network/data_out/RPI_clusters_seedling_cluster_heads2.json"
    edgelist = "../data_out/RPI_clusters_seedling_same_link_with_nil_d2.edgelist"
    outputfile = "../data_out/RPI_clusters_seedling_same_link_clusters_with_nil_attr_d2_0.9.jl"

    with open(edgelist) as edges:
        G.add_nodes_from(literal_eval(edges.readline()))
        for edge in edges:
            edge_nodes = literal_eval(edge)
            G.add_edge(edge_nodes[0], edge_nodes[1])

    cc = nx.connected_components(G)
    cluster_heads = json.load(open(path_to_cluster_heads))
    with open(outputfile, 'w') as output:
        for c in cc:
            answer = dict()
            answer['entities'] = map(lambda x:cluster_heads[x],list(c))
            json.dump(answer, output)
            output.write('\n')
            # output.write(str(c) + '\n')

if __name__ == '__main__':
    main(sys.argv[1:])
