def one_itemsets(minsup):

	# Get frequent 1 itemsets

	# Dictionary to track support
	category_dict = {}
	place_count = 0

	# Open File
	f = open("reviews_sample.txt", "r")

	# Iterate through each line of the text file
	for line in f:
		# Track the number of places
		place_count += 1
		# Separate each line into the individual words
		line = line.rstrip()
		categories = line.split(" ")
		line_tracker = set()
		for category in categories:
			# Check if it is in the dictionary, if not instantiate
			if category not in category_dict:
				category_dict[category] = 1
			# Otherwise add one
			elif category in line_tracker:
				continue
			else:
				category_dict[category] += 1
			line_tracker.add(category)

	f.close()

	# Only accept categories that meet the minsup
	minsup_abs = round(minsup * place_count)
	k_itemset_dict = {}
	for key in category_dict:
		if category_dict[key] >= minsup_abs:
			k_itemset_dict[key] = category_dict[key]
		else:
			continue

	return k_itemset_dict, minsup_abs

def print_dictionary(k_dict):

	# support:category
	for key in k_dict:
		#print(key)
		#print(key, k_dict[key])
		if type(key) == tuple:
			output = "{}:".format(k_dict[key]) 
			for category in key:
				output += category + ";"
			output = output[:-1]
			print(output)
		else:
			print("{}:{}".format(k_dict[key], key))

def contiguous_sequential_pattern_mine(k_dict, absolute_minsup):
	# In order to reference whether items are next to each other, we will have to reference the original dataset.
	# Key conditions:
	# We only need to see the pattern take place once in a line to add to the support. 
	# Need to turn length 1 words into length 2
	support_dict = {}
	# Get all possible 2 length itemsets
	permutation_set = set()
	for key in k_dict:
		for key2 in k_dict:
			permutation_set.add((key, key2))
	# Get all possible 2 length itemsets from each line and cross reference permutation list
	f = open("reviews_sample.txt", "r")
	for line in f:
		words_list = line.rstrip().split(" ")
		line_length = len(words_list)
		if line_length < 2:
			continue
		else:
			idx = 0
			line_tracker = set()
			while True:
				if idx == line_length-1:
					break
				matched = (words_list[idx], words_list[idx+1])
				if matched in permutation_set:
					if matched not in support_dict.keys():
						support_dict[matched] = 1
					elif matched in line_tracker:
						idx += 1
						continue
					else:
						support_dict[matched] += 1
				line_tracker.add(matched)
				idx += 1
	f.close()
	support_dict_minsup = {}
	for key in support_dict:
		if support_dict[key] >= absolute_minsup:
			support_dict_minsup[key] = support_dict[key]
		else:
			continue

	return support_dict_minsup

def cont_3(k_dict_2, absolute_minsup):
	# generate all possible permutations of 3 length itemsets from 2 length itemsets
	support_dict = {}
	permutation_set = set()
	for key in k_dict_2:
		for key2 in k_dict_2:
			if key[1] == key2[0]:
				permutation_set.add((key[0], key2[0], key2[1]))
			else:
					continue
	f = open("reviews_sample.txt", "r")
	for line in f:
		words_list = line.rstrip().split(" ")
		line_length = len(words_list)
		if line_length < 3:
			continue
		else:
			line_tracker = set()
			idx = 0
			while True:
				if idx == line_length-2:
					break
				matched = (words_list[idx], words_list[idx+1], words_list[idx+2])
				if matched in permutation_set:
					if matched in support_dict.keys():
						support_dict[matched] += 1
					elif matched in line_tracker:
						idx += 1
						continue
					else:
						support_dict[matched] = 1
				line_tracker.add(matched)
				idx += 1
	f.close()
	support_dict_minsup = {}
	for key in support_dict:
		if support_dict[key] >= absolute_minsup:
			support_dict_minsup[key] = support_dict[key]
		else:
			continue
	return support_dict_minsup

def main():
	minsup = 0.01
	k_dict_single, abs_minsup = one_itemsets(minsup)
	k_dict_2 = contiguous_sequential_pattern_mine(k_dict_single, abs_minsup)
	k_dict_3 = cont_3(k_dict_2, abs_minsup)
	print_dictionary(k_dict_single)
	print_dictionary(k_dict_2)

main()