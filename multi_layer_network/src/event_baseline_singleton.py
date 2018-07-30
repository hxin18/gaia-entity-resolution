import re
import sys
import json
import getopt
import gzip
from rdflib import Graph
from rdflib.term import Literal, URIRef, BNode
import codecs

from collections import defaultdict


def parse_line_into_triple(line):
	"""
    Convert a line into subject, predicate, object, and also a flag on whether object is a literal or URI.
    At present we assume all objects are URIs. Later this will have to be changed.
    :param line:
    :return:
    """
	# fields = re.split('> <', line[1:-2])
	# print fields
	answer = dict()
	g = Graph().parse(data=line, format='nt')
	for s, p, o in g:
		answer['subject'] = s
		answer['predicate'] = p
		answer['object'] = o

	if 'subject' not in answer:
		return None
	else:
		answer['isObjectURI'] = (type(answer['object']) != Literal)
		return answer

def event_baseline(path_to_KB_file, path_to_output, print_counter=False):
    """

    :param path_to_KB_file:
    :param path_to_output:
    :param print_counter:
    :return:
    """
    event_type_set = set()
    event_type_set.add('http://darpa.mil/aida/interchangeOntology#Event')
    TypeDict = dict()
    answer_dict = dict()
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if not (
                        'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in line or 'http://www.w3.org/2004/02/skos/core#prefLabel' \
                        in line or 'http://darpa.mil/aida/interchangeOntology#link' in line):
                continue
            # print 'yes'
            triple = parse_line_into_triple(line)
            if triple is None:
                continue
            if str(triple['predicate']) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' \
                    and str(triple['object']) in event_type_set:
                TypeDict[str(triple['subject'])] = str(triple['object'])
    out = codecs.open(path_to_output, 'w', 'utf-8')
    for k in TypeDict.keys():
        answer_dict['events'] = k
        json.dump(answer_dict, out)
        out.write('\n')
    out.close()

event_baseline('/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling.nt',
               '/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling_same_event_clusters.jl')
