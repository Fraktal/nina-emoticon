#! /usr/bin/python

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




#saving tweet_text_emoticon to pickle file to be used in word cloud and histogram
tweet_smiley = ' '.join([str(json.dumps(tweet["tweet_text_smiley"])) for tweet in tweet_smiley_mongo])

f_smiley = open("smiley_histo.pickle", "wb") 
pickle.dump(tweet_smiley, f_smiley)
f_smiley.close()



#sorting tweet_text for top 200 most frequent words             
N = 200
word_smiley = {} 

words_gen_smiley = (word.strip(punctuation).lower() for line in open('smiley_histo.pickle') 
                                                    for word in line.split())

for word in words_gen_smiley:
    word_smiley[word] = word_smiley.get(word, 0) + 1

top_words_smiley = sorted(word_smiley.iteritems(), key=itemgetter(1), reverse=True)[:N]


                                                  
#creating x and y variables for histogram
npopular = 200
total = len(set(word_smiley))
print total
x = []
y = range(npopular)
for pair in range(npopular):
    x = x + [top_words_smiley[pair][1]]
    print top_words_smiley[pair] 



#matplotlib histogram plot
fig = plt.figure()
fig.patch.set_facecolor('darkslategrey')
fig.patch.set_alpha(0.8)

ax = fig.add_subplot(111)
ax.patch.set_facecolor('#625858')
ax.patch.set_alpha(0.5)

plt.hist(x, bins=200, range = (0,1000), color = 'red', histtype = 'stepfilled') 
plt.xlabel('Frequency of Occurence: 0-1000')
plt.ylabel('Number of Words at Each Occurence')
plt.show()     