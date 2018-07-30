import re
import sys
import json
import getopt
import collections

from collections import defaultdict


### Given RPI ColdStart input, produces two JSON files: :Entity_strings and :String_strings. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:",["ifile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given RPI ColdStart input, produces two JSON files: :Entity_strings and :String_strings, usage: python get_strings.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg

	get_strings(inputfile)

def get_strings(path_to_KB_file):
	entity_types_and_strings = defaultdict(lambda: dict())
	string_strings = defaultdict(lambda: dict())

	with open(path_to_KB_file) as KB:
		for line in KB:
			if line.startswith(':Entity'):
				fields = re.split('\t', line)
				if len(fields) < 2: continue
				if fields[1] == 'type':
					entity_types_and_strings[fields[0]]['type'] = fields[2][:-1]
				elif 'mention' in fields[1]:
					entity_types_and_strings[fields[0]].setdefault('possible_strings', []).append(fields[2])
			elif line.startswith(':String'):
				fields = re.split('\t', line)
				if len(fields) < 2: continue
				if 'mention' in fields[1]:
					string_strings[fields[0]].setdefault('possible_strings', []).append(fields[2])

	for entity in entity_types_and_strings:
		counts = collections.Counter(entity_types_and_strings[entity]['possible_strings'])
		selected_string = max(counts.keys(), key=(lambda key: counts[key]))
		entity_types_and_strings[entity]['selected_string'] = selected_string

	for string in string_strings:
		counts = collections.Counter(string_strings[string]['possible_strings'])
		selected_string = max(counts.keys(), key=(lambda key: counts[key]))
		string_strings[string]['selected_string'] = selected_string

	with open(':String_strings.json', 'w') as output:
		json.dump(string_strings, output)

	with open(':Entity_strings.json', 'w') as output:
		json.dump(entity_types_and_strings, output)

if __name__ == '__main__':
	main(sys.argv[1:])
