import sys
import time

# start = time.time()
f = open(sys.argv[1], "r")
items_id = {}
count_single = {}
freq_items_id = {}
ids = 1
freq_ids = 1
support_threshold = 200

# give unique ids for items and count single items
for line in f:
    item_list = line.split()
    item_list = list(set(item_list))
    for item in item_list:
        if item not in items_id:
            items_id[item] = ids
            count_single[ids] = 1
            ids += 1
        else:
            count_single[items_id[item]] += 1
f.close()

# find frequent single items
for item_id in count_single:
    if (count_single[item_id] >= support_threshold):
        freq_items_id[item_id] = freq_ids
        freq_ids += 1
    else:
        freq_items_id[item_id] = 0

freq_ids -= 1

# generate triangular matrix for frequent items
# for pair(i,j), counts of pairs: tri_mat[i-1][j-i-1] 
tri_mat = []
for i in range(freq_ids -1):
    tri_mat.append([])
    for j in range(freq_ids - (i+1)):
        tri_mat[i].append(0)

# count pairs
f = open(sys.argv[1], "r")
for line in f:
    item_list = line.split()
    item_id_list = []
    for item in item_list:
        item_id_list.append(freq_items_id[items_id[item]])
    for i in range(freq_ids - 1):
        for j in range(freq_ids - (i+1)):
            if i+1 in item_id_list and i+j+2 in item_id_list:
                tri_mat[i][j] +=1
f.close()

# find freq pairs
freq_pairs = []
for i in range(freq_ids - 1):
    for j in range(freq_ids - (i+1)):
        if tri_mat[i][j] >= support_threshold:
            freq_pairs.append(((i+1, i+j+2), tri_mat[i][j]))
freq_pairs.sort(key =lambda x:-x[1])

# print results
# 1. # of frequent single itmes
# 2. # of frequent pairs
# 3. top 10 frequent pairs
print (freq_ids)
print (len(freq_pairs))

# take top 10 frequent pairs
top_pairs = []
for i in range(10):
    top_pairs.append(freq_pairs[i])
for pair in top_pairs:
    items = pair[0]
    count = pair[1]
    f_freq_id = items[0]
    s_freq_id = items[1]
    f_id = list(freq_items_id.keys())[list(freq_items_id.values()).index(f_freq_id)]
    s_id = list(freq_items_id.keys())[list(freq_items_id.values()).index(s_freq_id)]
    f_item = list(items_id.keys())[list(items_id.values()).index(f_id)]
    s_item = list(items_id.keys())[list(items_id.values()).index(s_id)]
    print ("%s\t%s\t%d" %(f_item, s_item, count))

# end = time.time()
# print("elapsed time = %f" %(end-start))