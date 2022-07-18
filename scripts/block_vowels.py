from collections import defaultdict
from math import ceil
import csv
import os
import random

if __name__ == "__main__":
	FOLDER = "../audio/vowel_segmented"
	OUTFILE = "../stimuli.csv"
	NUM_BLOCKS = 10

	filenames = os.listdir(FOLDER)
	groups = defaultdict(list)
	blocks = defaultdict(list)

	# Group vowel tokens according to vowel identity and gender
	for f in filenames:
		if f.split('.')[-1].lower() == 'textgrid':
			vowel, _, gender = f.split("_")[0:3]
			groups[(vowel[0], gender)].append(f)

	# Iterate through each group
	for group, tokens in groups.items():
		# Include a roughly equal number of tokens from each group in each block
		num_tokens = len(tokens)
		sample_sizes = [
			num_tokens // NUM_BLOCKS + (1 if x < num_tokens % NUM_BLOCKS else 0)
			for x in range(NUM_BLOCKS)
		]
		# Assign specific tokens to each block
		# First we randomize the order
		random.shuffle(tokens)
		# Then iterate through each block
		for block in range(NUM_BLOCKS):
			# Grab the number of samples we've assigned to this block
			num_samples = sample_sizes.pop()
			samples = tokens[-num_samples:]
			# Assign roughly half the samples to noise and half to quiet for the A order
			# and do the opposite assignment for the B order.
			half = len(samples) // 2
			a_order = ['noise'] * half + ['quiet'] * (len(samples) - half)
			b_order = ['quiet'] * half + ['noise'] * (len(samples) - half)
			
			# Store these associations
			blocks["{}-A".format(block)].extend(zip(a_order, samples))
			blocks["{}-B".format(block)].extend(zip(b_order, samples))
			
			# Remove tokens we've assigned to a block
			del tokens[-num_samples:]

	# Write the results to a file
	with open(OUTFILE, 'w') as f:
		out = csv.writer(f)
		headers = [
			'group', 'block' 'vowel', 'subject', 'gender', 
			'word', 'token_num', 'filename'
		]
		out.writerow(headers)
		for block, files in blocks.items():
			for condition, filename in files:
				row = [block, condition]
				row.extend(os.path.splitext(filename)[0].split('_') + [filename])
				out.writerow(row)