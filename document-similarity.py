import sys
import numpy as np
import time

# get shingle from each line
def get_shingle(line, k):
    i = 0
    while line[i] != " ":
        i += 1
    doc_content = line[(i+1):].lower()
    target_content = ""
    for char in doc_content:
        if char.isalpha() or char ==" ":
            target_content += char
    shingle = [target_content[j:j + k] for j in range(len(target_content) - k + 1)]
    res_shingle = list(set(shingle))
    res_shingle.sort()
    return res_shingle

# get id frome each line
def get_id(line):
    i = 0
    while line[i] != " ":
        i += 1
    return line[:i]

# find the smallest prime number larger than num 
def find_prime(num):
    is_prime = False
    while True:
        for i in range(2, num):
            rem = num % i
            if rem == 0:
                num += 1
                break
            if i == num-1: # here finds prime number
                is_prime = True
        if is_prime:
            return num

# hash k-shingles
def shingle_hash(str):
    p = 31
    m = 10**9+9
    power_of_p = 1
    hash_val = 0

    for i in range(len(str)):
        hash_val = ((hash_val + (ord(str[i]) -
                                 ord('a') + 1) *
                              power_of_p) % m)
 
        power_of_p = (power_of_p * p) % m
    return int(hash_val)

# hash integer list
def int_hash(int_list):
    c = 10**9
    res = 0
    for i in range(len(int_list)):
        res = (res + int_list[i]) % c
    return res

# for one hash function, get min value of all shingles in one document
def min_hash(shingle, a, b, c):
    res = 9999999
    for s in shingle:
        x = shingle_hash(s)
        res = min(res, (a*x+b) % c)
    return res

# get signature list for all shingles in one doc
def get_signature(c, shingle, rands):
    sig = []
    for r in rands:
        sig.append(int(min_hash(shingle, r[0], r[1], c))) # a = rand[0], b = rand[1]
    return sig

# get dictionary for bucket
# key: hash value of integers in each band
# value: indexes for candidate docs
def get_bucket(sig_mat, b, r):
    buckets = dict()
    for i in range(len(sig_mat)): # i: doc index
        sig_vals = sig_mat[i] # sig_vals: 120 hashed values of ith doc
        for j in range(b): # j: band index
            band = [sig_vals[k] for k in range(j*r, (j+1)*r)]
            band_hash = int_hash(band)
            if band_hash not in buckets:
                buckets[band_hash] = set()
            buckets[band_hash].add(i)
    return buckets

# check similarity of two colums in signature matrix
def check_sim(c1, c2, sig_mat):
    col_1 = sig_mat[c1]
    col_2 = sig_mat[c2]
    cnt = 0
    for i in range(len(col_1)):
        if col_1[i] == col_2[i]:
            cnt += 1
        else:
            continue
    rate = float(float(cnt)/float(len(col_1)))
    return rate

#===================
# start = time.time()
#===================
k = 3 # shingling with k
band = 6 # bands
row = 20 # rows for each band
n_tot = band * row # total rows
threshold = 0.9 # threshold

all_shingle_set = set()
shingle_list = [] # shingles for all docs
id_list = [] # ids for all docs
sig_mat = [] # final signature matrix len() = # of docs, len(ele) = # of hash functions

file = open(sys.argv[1], "r")
# get document id and shingles from each line
for line in file:
    shingle = get_shingle(line, k)
    doc_id = get_id(line)
    shingle_list.append(shingle)
    id_list.append(doc_id)
    all_shingle_set.update(shingle)
file.close()

n = len(all_shingle_set)
c = find_prime(n) # find smallest prime number larger than total # of shingles
random_values = [list(np.random.randint(1,c,size=2)) for i in range(n_tot)] # generate random hash functions

# make signature matrix
for shingle in shingle_list:
    sig = get_signature(c, shingle, random_values) # get signature values of one doc for all hash functions
    sig_mat.append(sig)

# dictionary for bucket
# key: hash value of integers of each band
# value: indexes for candidate docs
buckets = get_bucket(sig_mat, band, row)

cand_pair_list = list()
for b in buckets.values(): # in same bucket at least once -> candidate pairs
    cand_pair = set()
    if len(b) >= 2:
        for i in b:
            cand_pair.add(i)
    if len(cand_pair) >=2:
        cand_pair_list.append(list(cand_pair))

# make candidate pair to compare the column of signature matrix
cand_pair = set()
for l in cand_pair_list:
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            pair = (l[i], l[j]) if l[i] < l[j] else (l[j], l[i])
            cand_pair.add(pair)

# find similar documents from candidate pairs
sim_doc = list()
for pair in cand_pair:
    sim = check_sim(pair[0], pair[1], sig_mat) # compare sig_mat for cand1 and cand2
    if sim >= threshold: # similar documents found
        sim_doc.append(pair)

# print all similar document pairs
for ele in sim_doc:
    print ("%s\t%s" %(id_list[ele[0]], id_list[ele[1]]))

# end = time.time()
# print("elapsed time = %f" %(end-start))