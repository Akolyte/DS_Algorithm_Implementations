import math

def main():
    # testing information gain is working correctly
    i_list, t_list = read_input()
    dd_list = get_data(i_list)
    tt_list = get_data(t_list)
    #for d in dd_list:
         #print(d)
    #print("---------------------------------------------------")
    # split_dict = get_splits(dd_list)
    # print(split_dict, "splits")
    # print()
    # info_d = get_info_d(dd_list)
    # info_gain_dict = get_info_gain(dd_list, split_dict, info_d)
    # print(info_gain_dict, "info gain for corresponding split")
    tree = build_tree(dd_list, 2, 1)
    #print_tree(tree)
    for row in tt_list:
        prediction = predict(tree, row)
        print(prediction)
    #print(tt_list)
    
    
def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']

def build_tree(train, max_depth, min_size):
    root = get_node(train)
    split(root, max_depth, min_size, 1)
    return root

# get initial node object
def get_node(data_dict_list):
    b_index, b_value, b_score, b_branches = 999, 999, 999, None
    split_dict = get_splits(data_dict_list)
    info_gain_dict = get_info_gain(data_dict_list, split_dict, get_info_d(data_dict_list))
    split_value, attribute, index = get_best_split(info_gain_dict, split_dict)
    branches = split_data(attribute, split_value, data_dict_list)
    b_index, b_value, b_score, b_branches = attribute, split_value, info_gain_dict[attribute][index], branches
    #print(b_index, "index")
    #print(b_score, "gain score")
    #print(b_value, "attribute")
    return {'index':b_index, 'value':b_value, 'branches':b_branches}
    
# Create child splits for a node or make terminal
# needs work in progress, needs to have proper structure
def split(node, max_depth, min_size, depth):
    left, right = node['branches']
    del(node['branches'])
    # check for a no split
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        return
    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        return
    # process left child
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_node(left)
        split(node['left'], max_depth, min_size, depth+1)
    # process right child
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_node(right)
        split(node['right'], max_depth, min_size, depth+1)

def to_terminal(data_dict_list):
    outcomes = [row["label"] for row in data_dict_list]
    #print(outcomes)
    outcomes_count = {}
    for label in outcomes:
        if label not in outcomes_count:
            outcomes_count[label] = 1
        else:
            outcomes_count[label] += 1
    class_result = -1
    class_count = 0
    for outcome in outcomes_count:
        if outcomes_count[outcome] > class_count:
            class_result = outcome
            class_count = outcomes_count[outcome]
        elif outcomes_count[outcome] == class_count:
            if outcome < class_result:
                class_result = outcome
                class_count = outcomes_count[outcome]
            else:
                continue
        else:
            continue
        
    return class_result

# find max info gain split
# need to account for case where for two attributes they have an equal gain value, take the attribute with the smaller numerical value
def get_best_split(info_gain_dict, split_dict):
    max_gain = 0
    max_idx = 0
    max_attribute = None
    #print(info_gain_dict)
    #print(split_dict)
    for attribute in info_gain_dict:
        for i, gain in enumerate(info_gain_dict[attribute]):
            #print("{} >= {}".format(gain, max_gain))
            #print("{} <= {}".format(attribute, max_attribute))
            if gain > max_gain:
                max_gain = gain
                max_idx = i
                max_attribute = attribute
            elif gain == max_gain:
                if max_attribute == None or attribute < max_attribute:
                    max_gain = gain
                    max_idx = i
                    max_attribute = attribute
                else:
                    continue
            else:
                continue
    if max_gain != 0:
        max_split = split_dict[max_attribute][max_idx]
    else:
        max_split = 0
        max_attribute = 0
    return max_split, max_attribute, max_idx
    
def split_data(attribute, split_value, data_dict_list):
    left, right = list(), list()
    for row in data_dict_list:
        if row[attribute] <= split_value:
            left.append(row)
        else:
            right.append(row)
    return left, right
    
# Grab data from the input
def get_data(input_list):
    data_dict_list = []
    for row in input_list:
        row_dict = {}
        row_dict["label"] = int(row[0])
        for attribute_value_pairs in row[1:]:
            pairs = attribute_value_pairs.split(":")
            attribute = int(pairs[0])
            value = float(pairs[1])
            row_dict[attribute] = value
        data_dict_list.append(row_dict)
    return data_dict_list
    
# Get the split points for splits in decision tree for the root node
# Needs rewrite
def get_splits(data_dict_list):
    split_dict_init = {}
    # grab all the possible values that each attribute has
    for d in data_dict_list:
        row = d
        for k in row:
            if k == 'label':
                continue
            else:
                if k not in split_dict_init:
                    split_dict_init[k] = [row[k]]
                else:
                    if row[k] not in split_dict_init[k]:
                        split_dict_init[k].append(row[k])
                    else:
                        continue
    # sort the lists and remove duplicates
    split_dict_sorted = {}
    for attribute in split_dict_init:
        split_list = split_dict_init[attribute]
        split_list = sorted(split_list)
        split_dict_sorted[attribute] = split_list
        
    # get the actual splits from the sorted distinct lists of the values each attribute has
    split_dict = {}
    for attr in split_dict_sorted:
        a_max = len(split_dict_sorted[attr])
        curr = split_dict_sorted[attr]
        for a in range(0, a_max-1):
            split_pt = (curr[a] + curr[a+1]) / 2
            if attr not in split_dict:
                split_dict[attr] = [split_pt]
            elif split_pt not in split_dict[attr]:
                split_dict[attr].append(split_pt)
            else:
                continue
    return split_dict

def get_info_d(data_dict_list):
    total_rows = 0
    label_count_dict = {}
    # get labels and their counts
    for d in data_dict_list:
        curr_label = d["label"]
        if curr_label not in label_count_dict:
            label_count_dict[curr_label] = 1
        else:
            label_count_dict[curr_label] += 1
        total_rows += 1
    # calculate info(D)
    info_d = 0
    for label in label_count_dict:
        count = label_count_dict[label]
        info_d -= count / total_rows * math.log(count / total_rows, 2)
    return info_d

def get_info_gain(data_dict_list, split_list, info_d):
    # for each split point per attribute, we will find the information gain
    info_gain_dict = {}
    for attr in split_list:
        for pt in split_list[attr]:
            #print(pt, "split point")
            #print()
            curr_attr = {}
            for attr_dict in data_dict_list:
                label = attr_dict["label"]
                for attribute in attr_dict:
                    if attribute != "label":
                        value = attr_dict[attribute]
                        if attribute not in curr_attr:
                            curr_attr[attribute] = [(label, value)]
                        else:
                            curr_attr[attribute].append((label, value))
                    else:
                        continue
            # getting the info needed for each attribute
            # for each attribute we need to know 
            # 1. total # of rows, len will do just fine
            # 2. # of each class
            # 3/ # of each that pass or fail the current condition ( <= pt or threshold) with respect to class
            count = 0
            # 1.
            l = len(curr_attr[attr])
            class_dict = {}
            threshold_dict = {}
            for class_value_pair in curr_attr[attr]:
                # 2.
                clas = class_value_pair[0]
                value = class_value_pair[1]
                #print("{} value vs {} splitpt for label {}".format(value, pt, clas))
                if value <= pt and 0 not in threshold_dict:
                    threshold_dict[0] = 1
                    class_dict[0] = {clas:1}
                elif value > pt and 1 not in threshold_dict:
                    threshold_dict[1] = 1
                    class_dict[1] = {clas:1}
                elif value <= pt:
                    threshold_dict[0] += 1
                    if clas not in class_dict[0]:
                        class_dict[0][clas] = 1
                    else:
                        class_dict[0][clas] += 1
                elif value > pt:
                    threshold_dict[1] += 1
                    if clas not in class_dict[1]:
                        class_dict[1][clas] = 1
                    else:
                        class_dict[1][clas] += 1
                else:
                    continue
            info_a = 0
            #print(class_dict, "class_dict")
            #print(threshold_dict, "threshold_dict")
            for key in threshold_dict:
                label_cost = 0
                for label in class_dict[key]:
                    num = class_dict[key][label]
                    denom = threshold_dict[key]
                    #print("{} / {} * log({} / {})".format(num, denom, num, denom))
                    label_cost -= (num / denom * math.log(num/denom, 2))
                info_a += (threshold_dict[key] / l * label_cost)
                #print("{} / {} ratio".format(threshold_dict[key], l))

            #print(info_d, "info_d")
            #print(info_a, "info_a")
            info = info_d - info_a
            #print(info, "info")
            #print()
            if attr not in info_gain_dict:
                info_gain_dict[attr] = [info]
            else:
                info_gain_dict[attr].append(info)
            #print(info_gain_dict)
    return info_gain_dict

# read the input from the console
def read_input():
    input_list = []
    test_list = []
    while True:
        i = input()
        inp = i.split(" ")
        if int(inp[0]) != -1:
            input_list.append(inp)
        else:
            test_list.append(inp)
            break
    while True:
        try:
            i = input()
            inp = i.split(" ")
            test_list.append(inp)
        except EOFError as e:
            break
    return input_list, test_list

main()