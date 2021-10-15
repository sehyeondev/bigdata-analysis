import re
import sys
import math
import time
from pyspark import SparkConf, SparkContext

# make friend list from one line
def make_friend_list(line):
    line = line.split('\t')
    return (line[0], line[1].split(','))

# make pairs
# ((user, friend), 0) ((friend, friend), 2)
def make_pair(user_friends):
    res = []
    user = user_friends[0] # u1
    f = user_friends[1] # friend list [1,2,3]
    for i in range(len(f)):
        uf_pair = ((user, f[i]), 0) if (user < f[i]) else ((f[i], user), 0)
        res.append(uf_pair)
        for j in range(i+1, len(f)):
            ff_pair = ((f[i], f[j]), 2) if (f[i] < f[j]) else ((f[j], f[i]), 2)
            res.append(ff_pair)
    return res

# start = time.time()

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
user_friends = lines.map(lambda l: make_friend_list(l)) # [[u1,[0,1,2]], [u2,[0,2,3]], ...]
pairs = user_friends.flatMap(lambda l: make_pair(l)) # ((user, friend), 0) ((friend, friend), 2)
count_commons = pairs.reduceByKey(lambda x, y: x*y) # if keys are friends each other -> value = 0
result_pairs = count_commons.filter(lambda p: p[1] != 0) # keys have n common friends -> value = 2^n
result_pairs = result_pairs.sortBy(lambda x: x[0][0]) # sort by first user
result_pairs = result_pairs.sortBy(lambda x: x[0][1])
sorted_pairs = result_pairs.sortBy(lambda x: -x[1]) # sort by count in descending order
top_result = sorted_pairs.take(10) # take top 10 key-value pairs

# print results
for ele in top_result:
    print("%s\t%s\t%d" %(ele[0][0], ele[0][1], math.log2(ele[1])))
sc.stop()

# end = time.time()
# print("elapsed time = %f" %(end-start))