from pylab import *
from scipy import *
import sys, time
import webbrowser
import pymongo
from pymongo import Connection  
from bson import BSON
from bson.json_util import dumps
from bson import Code
from bson.son import SON
import json
import cPickle as pickle
import simplejson
from string import punctuation
from operator import itemgetter
import operator, time, string
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
import nltk
from datetime import datetime
import collections


#mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweetDB']


#group by tweet_text_emoticon from mongo
reducer = Code("""
                   function(obj, prev){
                     prev.count++;
                   }
                   """)
tweet_smiley_mongo = db.tweets.group(key={"tweet_text_smiley":1}, condition={}, initial={"count": 0}, 
                                             reduce=reducer)

tweet_smiley = ' '.join([str(json.dumps(tweet["tweet_text_smiley"])) for tweet in tweet_smiley_mongo])


#file to for sorting top words
f_smiley = open("smiley.txt", "wb") 
pickle.dump(tweet_smiley, f_smiley)
f_smiley.close()



#sorting tweet_text for top 2000 most frequent words             
N = 2000
word_smiley = {} 

words_gen_smiley = (word.strip(punctuation).lower() for line in open('smiley.txt') 
                                                    for word in line.split())

for word in words_gen_smiley:
    word_smiley[word] = word_smiley.get(word, 0) + 1

top_words_smiley = sorted(word_smiley.iteritems(), key=itemgetter(1), reverse=True)[:N]

npopular = 100

data = [tuple(top_words_smiley)
        for pair in top_words_smiley(pair[1])
        for c in range(npopular)]
count = collections.Counter(data)

points = count.keys()
x, y = zip(*points)
sizes = np.array(count.values())**2
plt.scatter(x, y, s=sizes, marker='o', c=sizes)
plt.show()