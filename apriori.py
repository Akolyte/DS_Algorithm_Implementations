def one_itemsets(minsup):

	# Get frequent 1 itemsets

	# Dictionary to track support
	category_dict = {}
	place_count = 0

	# Open File
	f = open("categories.txt", "r")

	# Iterate through each line of the text file
	for line in f:
		# Track the number of places
		place_count += 1
		# Separate each line into the individual words
		line = line.rstrip()
		categories = line.split(";")
		for category in categories:
			# Check if it is in the dictionary, if not instantiate
			if category not in category_dict:
				category_dict[category] = 1
			# Otherwise add one
			else:
				category_dict[category] += 1

	f.close()

	# Only accept categories that meet the minsup
	minsup_abs = round(minsup * place_count)
	k_itemset_dict = {}
	for key in category_dict:
		if category_dict[key] >= minsup_abs:
			k_itemset_dict[key] = category_dict[key]
		else:
			continue

	return k_itemset_dict, place_count

def apriori_2_itemset(minsup):

	k_dict, place_count = one_itemsets(minsup)
	k = 2
	current_dict = {}
	newSet = set()

	while True:

	# Repeat
		# Generate (k+1) itemsets from k itemsets
		for key in k_dict:
			if type(key) == str:
				newSet.add(frozenset([key]))
			else:
				newSet.add(key)
		candidates = getJoin(newSet, k)
		# Test the candidates against the DB
		f = open("categories.txt", "r")		
		for line in f:
			line = line.rstrip()
			categories = line.split(";")
			category_set = set(categories)
			for candidate in candidates:
				if candidate.issubset(category_set) and candidate not in current_dict:
					current_dict[candidate] = 1
				elif candidate.issubset(category_set):
					current_dict[candidate] += 1
				else:
					continue
		minsup_abs = round(minsup * place_count)
		for key in current_dict:
			if current_dict[key] >= minsup_abs:
				k_dict[key] = current_dict[key]
			else:
				continue
		# Unitl no frequent or candidate set can be generated
		if bool(current_dict) == False:
			break
		else:
			# Set k = k + 1
			k += 1
			newSet = set()
			current_dict = {}

	return k_dict

def getJoin(itemSet, length):
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

def print_apriori_result(k_dict):

	# support:category
	for key in k_dict:
		#print(key)
		#print(key, k_dict[key])
		if type(key) == frozenset:
			output = "{}:".format(k_dict[key]) 
			for category in key:
				output += category + ";"
			output = output[:-1]
			print(output)
		else:
			print("{}:{}".format(k_dict[key], key))

def main():
	minsup = 0.01
	#k_dict = apriori_2_itemset(minsup)
	k_dict_single, place_count = one_itemsets(minsup)
	#print_apriori_result(k_dict)
	print_apriori_result(k_dict_single)

main()