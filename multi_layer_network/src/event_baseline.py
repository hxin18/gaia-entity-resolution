import re
import sys
import json
import getopt
import numpy as np
import networkx as nx

from datetime import datetime
from collections import defaultdict


### Given events JSON file, outputs events linkings in the format of connected components according to baseline #1. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given events JSON file, outputs events linkings in the format of connected components according to baseline #1, usage: python event_baseline.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	
	event_baseline_linking(inputfile, outputfile)

def event_baseline_linking(path_to_events, path_to_output):
	events = json.load(open(path_to_events))

	IDs = list(events.keys())

	G = nx.Graph()
	G.add_nodes_from(IDs)

	for i, id1 in enumerate(IDs):
		for j in range(i + 1, len(IDs)):
			id2 = IDs[j]

			if events[id1]['type'] == events[id2]['type'] and events[id1]['text'] == events[id2]['text']:
				if len(re.split('_', events[id1]['doc'])) == 5:
					id1_temporal_info = re.split('_', events[id1]['doc'])[3]
				# NYT Exception
				elif events[id1]['doc'][0:3] == 'NYT':
					id1_temporal_info = re.split('_', events[id1]['doc'])[2][0:8]
				if len(re.split('_', events[id2]['doc'])) == 5:
					id2_temporal_info = re.split('_', events[id2]['doc'])[3]
				# NYT Exception
				elif events[id2]['doc'][0:3] == 'NYT':
					id2_temporal_info = re.split('_', events[id2]['doc'])[2][0:8]
				id1_datetime = datetime.strptime(id1_temporal_info, '%Y%m%d')
				id2_datetime = datetime.strptime(id2_temporal_info, '%Y%m%d')

				difference = abs((id1_datetime - id2_datetime).days)

				if difference < 3:
					G.add_edge(id1, id2)

	print('Graph construction done!')

	cc = nx.connected_components(G)

	with open(path_to_output, 'w') as output:
		for c in cc:
			output.write(str(c) + '\n')

if __name__ == '__main__':
	main(sys.argv[1:])
