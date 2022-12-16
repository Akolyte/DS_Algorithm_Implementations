def main():
    unique_features_count_dict = {"hair":[0, 1], "feathers":[0, 1], "eggs":[0, 1], "milk":[0, 1], "airborne":[0, 1], "aquatic":[0, 1], "predator":[0, 1], "toothed":[0, 1], "backbone":[0, 1], "breathes":[0, 1], "venomous":[0, 1], "fins":[0, 1], "legs":[0, 2, 4, 5, 6, 8], "tail":[0, 1], "domestic":[0, 1], "catsize":[0, 1]}
    train, test = read_data()
    pc_dict = naive_bayes_y(train)
    pfc_dict = naive_bayes_xy(train, unique_features_count_dict)
    # We will now get joint probability of each class for the test rows
    for row in test:
        print(joint_probability(row, pfc_dict, pc_dict))
    
def joint_probability(row, pfc_dict, pc_dict):
    clas_joint_prob_dict = {}
    for clas in pc_dict:
        total_value = 1
        for attribute in row:
            if attribute == "animal_name" or attribute == "class_type":
                continue
            else:
                value = row[attribute]
                # key value of pfc_dict consists of (value, attribute, and class)
                total_value *= pfc_dict[value, attribute, clas]
        class_probability = pc_dict[clas] * total_value
        clas_joint_prob_dict[clas] = class_probability
    max_prob = 0
    max_class = None
    for c in clas_joint_prob_dict:
        if clas_joint_prob_dict[c] > max_prob:
            max_prob = clas_joint_prob_dict[c]
            max_class = c
        else:
              continue
    return max_class
    
def naive_bayes_xy(train, feature_unique_value_cnt):
    class_set = set()
    pfc_dict = {}
    
    # get unique classes
    for row2 in train:
        class_set.add(row2["class_type"])
    while len(class_set) > 0:
        pfcv_dict = {}
        curr_class = class_set.pop()
        class_count = 0
        for row in train:
            if row["class_type"] == curr_class:
                class_count += 1
            else:
                continue
            # 1 -> True, 0 -> False technically doesn't matter thanks to joint probability!!!
            for attribute in row:
                value = row[attribute]
                if row["class_type"] != curr_class:
                    continue
                elif attribute == "animal_name" or attribute == "class_type":
                    continue
                elif (value, attribute) not in pfcv_dict:
                    pfcv_dict[(value, attribute)] = 1
                else:
                    pfcv_dict[(value, attribute)] += 1
        #print(pfcv_dict)
        #print(class_count, "class_count")
        #print()
        for feature in feature_unique_value_cnt:
            total_value = 1
            for value in feature_unique_value_cnt[feature]:
                #print("{} value {} feature".format(value, feature))
                if (value, feature) not in pfcv_dict:
                    count = 0
                else:
                    count = pfcv_dict[(value, feature)]
                # equation 2
                pfc_dict[(value, feature, curr_class)] = ((count + 0.1) / ((class_count + 0.1)* len(feature_unique_value_cnt[feature])))
            #print(total_value)
    return pfc_dict
    
def naive_bayes_y(train):
    class_set = set()
    N = 0
    for row in train:
        class_set.add(row["class_type"])
        N += 1
    C = len(class_set)
    pc_dict = {}
    while len(class_set) > 0:
        curr_class = class_set.pop()
        class_count = 0
        for row in train:
            if row["class_type"] == curr_class:
                class_count += 1
            else:
                continue
        # equation 1
        pc_dict[curr_class] = (class_count + 0.1) / (N + 0.1 * C)
    return pc_dict

def read_data():
    train_data = []
    test_data = []
    attributes = input()
    attr_list = attributes.split(",")
    firstrow = True
    while True:
        row = input()
        idx_list = row.split(",")
        if idx_list[-1] == "-1":
            idx_list = row.split(",")
            curr_dict = {}
            for idx in range(0, len(attr_list)):
                if idx == 0:
                    curr_dict[attr_list[idx]] = idx_list[idx]
                else:
                    curr_dict[attr_list[idx]] = int(idx_list[idx])
            test_data.append(curr_dict)
            break
        else:
            curr_dict = {}
            for idx in range(0, len(attr_list)):
                if idx == 0:
                    curr_dict[attr_list[idx]] = idx_list[idx]
                else:
                    curr_dict[attr_list[idx]] = int(idx_list[idx])
            train_data.append(curr_dict)
    while True:
        try: 
            row = input()
            idx_list = row.split(",")
            curr_dict = {}
            for idx in range(0, len(attr_list)):
                if idx == 0:
                    curr_dict[attr_list[idx]] = idx_list[idx]
                else:
                    curr_dict[attr_list[idx]] = int(idx_list[idx])
            test_data.append(curr_dict)
        except EOFError as e:
            break
    return train_data, test_data

main()