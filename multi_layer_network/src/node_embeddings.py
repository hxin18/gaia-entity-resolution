import sys
import json
import getopt
import numpy as np

### Given the canonical mentions JSON file and an embeddings file, produces the node embeddings. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:e:o:",["ifile=","efile=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given the canonical mentions JSON file and an embeddings file, produces the node embeddings, usage: python node_embeddings.py -i <inputjsonfile> -e <embeddingsfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-e", "--efile"):
			embeddingsfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	cluster_heads = json.load(open(inputfile))
	
	# needed_words = set()

	# for cluster_head in cluster_heads:
	# 	needed_words.update(cluster_heads[cluster_head][0][1:-1].split())

	# print(len(needed_words))

	# with open('wiki.en.vec') as fasttext, open('needed_words.vec', 'w') as needed_words_vec_file:
	# 	for line in fasttext:
	# 		if line.split()[0] == 'oov' or line.split()[0] in needed_words:
	# 			print(line.split()[0])
	# 			needed_words_vec_file.write(line)

	
	word_vecs = {}

	with open(embeddingsfile) as word_vecs_file:
		for line in word_vecs_file:
			try:
				word = line[:-1].split()[0]
				vec = np.array([float(x) for x in line[:-1].split()[1:]])
				word_vecs[word] = vec
			except:
				continue

		vec_size = len(vec)

	with open(outputfile, 'w') as cluster_heads_vec_file:
		for cluster_head in cluster_heads:
			cluster_head_words = cluster_heads[cluster_head][0][1:-1].split()
			vec = np.zeros(vec_size)
			for word in cluster_head_words:
				vec += word_vecs.get(word, word_vecs['oov'])
			vec = vec / len(cluster_head_words)
			cluster_heads_vec_file.write(cluster_head + ' ' + ' '.join([str(x) for x in vec.tolist()]) + '\n')

if __name__ == '__main__':
	main(sys.argv[1:])
