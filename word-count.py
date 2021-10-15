import re
import sys
from pyspark import SparkConf, SparkContext

# make all words lower
def f(word):
    word = word.lower()
    return word

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
words = lines.flatMap(lambda l: re.split(r'[^\w]+', l))

words = words.map(f).distinct() #make all words lower
words = words.filter(lambda w: w != '') #eliminate the blank
words = words.filter(lambda w: w[0].isalpha() == True) #extract the words starts with alphabet
pairs = words.map(lambda w: (w[0],1)) #make key-value pairs (key: first character of the word, value: 1)
counts = pairs.reduceByKey(lambda n1, n2: n1+n2).sortByKey() #count the words with same key and sort in alphabetical order
result = counts.collect()

#print the result
for ele in result:
    print("%s\t%d" %(ele[0], ele[1]))
sc.stop()