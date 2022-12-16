# Implement the k-means algorithm and apply it to a real-life data set

# Euclidean distance (L1) (3 Clusters)

# Imathut format "-112.1, 33.5" "longitude", "latitude"
# Output format "location_id, cluster_label" -> clusters.txt

import math

from statistics import mean

from random import randint

def read_file():
	f = open("places.txt", "r")
	coord_list = []
	for line in f:
		coordinates = line.rstrip().split(",")
		t_list = []
		for coord in coordinates:
			c = float(coord)
			t_list.append(c)
		coord_list.append(t_list)
	return coord_list

def k_means(coord_list):
	c1, c2, c3 = init_clusters(coord_list)
	epoch = 0
	prev_c1 = c1
	prev_c2 = c2
	prev_c3 = c3

	while epoch < 100:
		c1_list = []
		c2_list = []
		c3_list = []
		# Find new clusters
		for i, coord in enumerate(coord_list):
			c1_dist = distance(coord, c1)
			c2_dist = distance(coord, c2)
			c3_dist = distance(coord, c3)
			if c1_dist <= c2_dist and c1_dist <= c3_dist:
				c1_list.append(coord)
			elif c2_dist <= c1_dist and c2_dist <= c3_dist:
				c2_list.append(coord)
			else:
				c3_list.append(coord)

		# c3
		list1 = []
		list2 = []
		for tup1 in c1_list:
			list1.append(tup1[0])
			list2.append(tup1[1])
		c1 = (mean(list1), mean(list2))

		# c2
		list1 = []
		list2 = []
		for tup2 in c2_list:
			list1.append(tup2[0])
			list2.append(tup2[1])
		c2 = (mean(list1), mean(list2))

		# c3
		list1 = []
		list2 = []
		for tup3 in c3_list:
			list1.append(tup3[0])
			list2.append(tup3[1])
		c3 = (mean(list1), mean(list2))

		# convergance
		if prev_c1 == c1 and prev_c2 == c2 and prev_c3 == c3:
			print(convergance)
			break
		
		epoch += 1

	# Get results

	result_dict = {}
	for i, coord in enumerate(coord_list):
		c1_dist = distance(coord, c1)
		c2_dist = distance(coord, c2)
		c3_dist = distance(coord, c3)
		if c1_dist <= c2_dist and c1_dist <= c3_dist:
			result_dict[i] = 1
		elif c2_dist <= c1_dist and c2_dist <= c3_dist:
			result_dict[i] = 2
		else:
			result_dict[i] = 3

	for key in result_dict:
		print("{} {}".format(key, result_dict[key]))

	return result_dict


def init_clusters(coord_list):
	list1 = []
	list2 = []
	for tup in coord_list:
		list1.append(tup[0])
		list2.append(tup[1])
	min_list1 = int(min(list1))
	max_list1 = int(max(list1))
	min_list2 = int(min(list2))
	max_list2 = int(max(list2))
	c1 = [float(randint(min_list1,max_list1)),float(randint(min_list2,max_list2)), float(randint(min_list1,max_list1)),float(randint(min_list2,max_list2))]
	c2 = [float(randint(min_list1,max_list1)),float(randint(min_list2,max_list2)), float(randint(min_list1,max_list1)),float(randint(min_list2,max_list2))]
	c3 = [float(randint(min_list1,max_list1)),float(randint(min_list2,max_list2)), float(randint(min_list1,max_list1)),float(randint(min_list2,max_list2))]

	return c1, c2, c3

def distance(coord1, coord2):
	dist = math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)
	return dist

def main():
	c_list = read_file()
	results = k_means(c_list)
	
main()