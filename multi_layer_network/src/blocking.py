import re
import sys
import json
import getopt
import gzip

from collections import defaultdict



def main(argv):
	opts, _ = getopt.getopt(argv,"hi:a:o:",["ifile=","algo=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given cluster_head RPI_to_JSON.py output for entities block the entities into non-overlapping clusters'
				  'Produces one JSON file per block; usage: python blocking.py -i <inputfile> -a <algorithm: select from 1> -o <outputfolder>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-a", "--algo"):
			algorithm = int(arg)
		elif opt in ("-o", "--ofile"):
			outputfolder = arg

	if algorithm == 1:
		blocking_alg1(inputfile, outputfolder)
	elif algorithm == 2:

		blocking_alg2(inputfile, outputfolder)

	elif algorithm == 3:

		blocking_alg3(inputfile, outputfolder)
	else:
		raise Exception

def blocking_alg1(path_to_cluster_heads, path_to_output_folder):
	"""
	This blocking algorithm does the following very simple test. if two entities have the same type, they are blocked to the same block.
	:param path_to_cluster_heads:
	:param path_to_output_folder:
	:return:
	"""
	cluster_heads = json.load(open(path_to_cluster_heads))
	bkv_blocks = dict()
	for k, v in cluster_heads.items():

		if v[1] not in bkv_blocks:
			bkv_blocks[v[1]] = dict()
		bkv_blocks[v[1]][k] = v

	for k, v in bkv_blocks.items():
		json.dump(v,open(path_to_output_folder+str(k)+'.json', 'w'))

def blocking_alg2(path_to_cluster_heads, path_to_output_folder):
	"""
	if two entities have the same type and occur on the same DAY, they are blocked to the same block.
	:param path_to_cluster_heads:
	:param path_to_output_folder:
	:return:
	"""
	cluster_heads = json.load(open(path_to_cluster_heads))
	bkv_blocks = dict()
	for k, v in cluster_heads.items():
		timestamp = re.split('_',k)[-2]
		bkv = v[1]+'_'+timestamp
		if bkv not in bkv_blocks:
			bkv_blocks[bkv] = dict()
		bkv_blocks[bkv][k] = v

	for k, v in bkv_blocks.items():
		json.dump(v,open(path_to_output_folder+str(k)+'.json', 'w'))

def blocking_alg3(path_to_cluster_heads, path_to_output_folder):
	"""
	if two entities have the same type and occur on the same MONTH, they are blocked to the same block.
	:param path_to_cluster_heads:
	:param path_to_output_folder:
	:return:
	"""
	cluster_heads = json.load(open(path_to_cluster_heads))
	bkv_blocks = dict()
	for k, v in cluster_heads.items():
		timestamp = re.split('_',k)[-2]
		bkv = v[1]+'_'+timestamp[0:6]
		if bkv not in bkv_blocks:
			bkv_blocks[bkv] = dict()
		bkv_blocks[bkv][k] = v

	for k, v in bkv_blocks.items():
		json.dump(v,open(path_to_output_folder+str(k)+'.json', 'w'))


if __name__ == '__main__':
	main(sys.argv[1:])
